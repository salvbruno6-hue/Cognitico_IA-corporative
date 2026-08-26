"""HTTP API mínima do ELO Control Plane, usando somente biblioteca padrão."""
from __future__ import annotations
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .elo_control_plane import ELOControlPlane, PolicyError

HOST = os.getenv("ELO_HOST", "0.0.0.0")
PORT = int(os.getenv("ELO_PORT", "8080"))
CORE = ELOControlPlane()

class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/v1/status":
            return self._send(200, {"service": "elo-control-plane", "status": "ok"})
        if self.path == "/v1/schema":
            return self._send(200, {"operations": ["query", "plan"], "policy": "deny-by-default"})
        self._send(404, {"error": "not_found"})

    def do_POST(self):
        if self.path not in ("/v1/query", "/v1/plan"):
            return self._send(404, {"error": "not_found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            text = payload.get("query") or payload.get("text")
            if not isinstance(text, str) or not text.strip():
                return self._send(400, {"error": "query_required"})
            operation = payload.get("operation", "read")
            if self.path == "/v1/plan":
                return self._send(200, CORE.plan(text, operation))
            return self._send(200, CORE.handle(text, operation))
        except PolicyError as exc:
            return self._send(403, {"error": str(exc)})
        except (ValueError, json.JSONDecodeError):
            return self._send(400, {"error": "invalid_json"})

    def log_message(self, fmt, *args):
        return

if __name__ == "__main__":
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
