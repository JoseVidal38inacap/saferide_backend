import json
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from kafka import KafkaConsumer, errors as kafka_errors

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("alerts_service")

KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]
KAFKA_TOPICS = ["trip.created", "trip.finished", "payment.completed"]


def process_alert(event: dict, topic: str) -> None:
    """
    Lógica simple de alertas para distintos eventos.
    """
    if topic == "trip.finished":
        logger.info(
            "AlertsService: viaje %s finalizado. Posible alerta de feedback.",
            event.get("id"),
        )
    elif topic == "trip.created":
        logger.info(
            "AlertsService: nuevo viaje creado para pasajero %s.",
            event.get("passenger"),
        )
    elif topic == "payment.completed":
        logger.info(
            "AlertsService: pago completado para trip %s.",
            event.get("trip_id"),
        )
    else:
        logger.info(
            "AlertsService: evento recibido en %s: %s", topic, event
        )


def consume_events() -> None:
    try:
        consumer = KafkaConsumer(
            *KAFKA_TOPICS,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            group_id="alerts-service",
            auto_offset_reset="earliest",
        )
        logger.info(
            "AlertsService conectado a Kafka. Escuchando topics %s",
            ", ".join(KAFKA_TOPICS),
        )
    except kafka_errors.NoBrokersAvailable as exc:
        logger.error("AlertsService: Kafka no disponible: %s", exc)
        return

    for message in consumer:
        event = message.value
        topic = message.topic
        logger.info("AlertsService: evento recibido en %s: %s", topic, event)
        process_alert(event, topic)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                b'{"status": "ok", "service": "alerts-service"}'
            )
        else:
            self.send_response(404)
            self.end_headers()


def run_health_server(port: int = 8003) -> None:
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    logger.info(
        "AlertsService health-check en http://localhost:%s/health", port
    )
    server.serve_forever()


if __name__ == "__main__":
    consumer_thread = threading.Thread(target=consume_events, daemon=True)
    consumer_thread.start()
    run_health_server()
