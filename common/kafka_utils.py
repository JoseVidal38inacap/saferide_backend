import json
import logging
from typing import Any, Dict, Optional

from kafka import KafkaProducer

logger = logging.getLogger(__name__)

_producer: Optional[KafkaProducer] = None


def get_producer() -> Optional[KafkaProducer]:
    """
    Crea (si hace falta) y retorna un productor Kafka.
    Si no se puede conectar, deja el productor en None
    y registra el error en los logs.
    """
    global _producer

    if _producer is not None:
        return _producer

    try:
        _producer = KafkaProducer(
            bootstrap_servers=["localhost:9092"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        logger.info("Kafka producer creado correctamente")
    except Exception as exc:  # pragma: no cover
        logger.error("No se pudo crear el KafkaProducer: %s", exc)
        _producer = None

    return _producer


def send_event(topic: str, payload: Dict[str, Any]) -> None:
    """
    Envía un evento a Kafka. Si Kafka no está disponible,
    solo se deja un warning en logs (la API sigue funcionando).
    """
    producer = get_producer()
    if producer is None:
        logger.warning(
            "Kafka no disponible, evento NO enviado. Topic=%s, payload=%s",
            topic,
            payload,
        )
        return

    try:
        producer.send(topic, payload)
        producer.flush()
        logger.info("Evento enviado a Kafka. Topic=%s, payload=%s", topic, payload)
    except Exception as exc:  # pragma: no cover
        logger.error("Error enviando evento a Kafka: %s", exc)
