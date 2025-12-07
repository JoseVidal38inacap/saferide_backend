import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] notifier: %(message)s")

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "ok",
                "service": "notifier-service",
                "timestamp": datetime.utcnow().isoformat()
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server = HTTPServer(("localhost", 8002), HealthHandler)
    logging.info("NotifierService escuchando en http://localhost:8002/health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("NotifierService detenido")
    finally:
        server.server_close()

if __name__ == "__main__":
    logging.info("Levantando Notifier Service...")
    run_server()
