"""Local IPC handler for the render daemon (line-delimited JSON over TCP)."""
from __future__ import annotations

import json
import logging
import socketserver
from typing import Any

log = logging.getLogger(__name__)


class _Handler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        for raw in self.rfile:
            try:
                msg: dict[str, Any] = json.loads(raw)
            except json.JSONDecodeError:
                self.wfile.write(b'{"error":"bad json"}\n')
                continue
            cmd = msg.get("cmd")
            if cmd == "ping":
                self.wfile.write(b'{"ok":true}\n')
            elif cmd == "render":
                self.wfile.write(b'{"ok":true,"accepted":true}\n')
            else:
                self.wfile.write(b'{"error":"unknown cmd"}\n')


class RenderDaemon(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, host: str = "127.0.0.1", port: int = 8767) -> None:
        super().__init__((host, port), _Handler)