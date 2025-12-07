import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] billing-service: %(message)s",
)

FAKE_METRICS = {
    "total_trips_billed": 42,
    "total_revenue": 350000,  # pesos chilenos simulados
    "currency": "CLP",
}


class BillingHandler(BaseHTTPRequestHandler):
    def _send_json(self, data: dict, status_code: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "ok",
                "service": "billing-service",
                "timestamp": datetime.utcnow().isoformat(),
            }
            self._send_json(response)

        elif self.path == "/metrics":
            # En un sistema real, aquí se consultarían pagos reales desde el backend.
            response = {
                "status": "ok",
                "service": "billing-service",
                "metrics": FAKE_METRICS,
                "generated_at": datetime.utcnow().isoformat(),
            }
            self._send_json(response)

        else:
            self._send_json({"detail": "Not found"}, status_code=404)


def run_server(port: int = 8003):
    server = HTTPServer(("localhost", port), BillingHandler)
    logging.info(
        "BillingService escuchando en http://localhost:%s/health y /metrics",
        port,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("BillingService detenido")
    finally:
        server.server_close()


if __name__ == "__main__":
    logging.info("Levantando BillingService...")
    run_server()
