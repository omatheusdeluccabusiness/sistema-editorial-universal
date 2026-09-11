#!/usr/bin/env python3
from __future__ import annotations

import base64
import functools
import html
import http.server
import io
import json
import os
import re
import secrets
import socketserver
import sys
import tempfile
import urllib.parse
import zipfile
from pathlib import Path

try:
    from scripts.hub_sessions import create_hub_session, hub_session_needs_refresh, refresh_hub_session
    from scripts.template_catalog import public_template_catalog
except ImportError:
    from hub_sessions import create_hub_session, hub_session_needs_refresh, refresh_hub_session
    from template_catalog import public_template_catalog


PROJECT_ROOT = Path(__file__).resolve().parent.parent
HUB_TEMPLATE = PROJECT_ROOT / "templates" / "hub.html"
EDITOR_DIR = Path(os.environ.get("CARROSSEL_EDITOR_DIR", str(Path(tempfile.gettempdir()) / "carrossel-editor-universal")))
PORT = int(os.environ.get("CARROSSEL_EDITOR_PORT", "8797"))
CSRF_TOKEN = secrets.token_urlsafe(32)
ALLOWED_SESSIONS = r"hub-(tweet|stories|stories-fundo|notes)-[0-9a-f]{12}"
EDITOR_DIR.mkdir(parents=True, exist_ok=True)


def _runtime(html_text: str) -> str:
    payload = (
        "<script>window.CARROSSEL_CSRF="
        + json.dumps(CSRF_TOKEN)
        + ";document.addEventListener('DOMContentLoaded',()=>{"
        + "['btn-send-tg','btn-config-tg','btn-publish-ig'].forEach(id=>{"
        + "const node=document.getElementById(id);const group=node&&(node.closest('.inspector-section')||node.closest('.inspector-group'));"
        + "if(group)group.style.display='none';else if(node)node.style.display='none';});"
        + "});</script>"
    )
    marker = "</head>" if "</head>" in html_text else "</body>"
    return html_text.replace(marker, payload + marker, 1)


def _hub() -> str:
    catalog = json.dumps(public_template_catalog(), ensure_ascii=False).replace("</", "<\\/")
    return _runtime(HUB_TEMPLATE.read_text(encoding="utf-8").replace("{{TEMPLATES_JSON}}", catalog))


class Handler(http.server.SimpleHTTPRequestHandler):
    server_version = "CarouselEditorUniversal/1.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(EDITOR_DIR), **kwargs)

    def _json(self, status: int, value: dict) -> None:
        payload = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _html(self, status: int, value: str) -> None:
        payload = value.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length) if length else b"{}"
        value = json.loads(payload)
        if not isinstance(value, dict):
            raise ValueError("O corpo deve ser um objeto JSON.")
        return value

    def _authorized(self) -> bool:
        host = (self.headers.get("Host") or "").split(":", 1)[0].lower()
        return host in {"localhost", "127.0.0.1"} and self.headers.get("X-Carrossel-CSRF") == CSRF_TOKEN

    def do_GET(self) -> None:
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/health":
            return self._json(200, {"ok": True, "service": "editor-carrosseis-universal"})
        if path in {"", "/", "/index.html"}:
            return self._html(200, _hub())
        if path == "/api/telegram/status":
            return self._json(200, {"configured": False})

        safe_assets = {
            "/HorshamSerial.otf": PROJECT_ROOT / "HorshamSerial.otf",
            "/assets/fonts/GaramondModern-Regular.otf": PROJECT_ROOT / "assets/fonts/GaramondModern-Regular.otf",
            "/assets/fonts/Advercase-Regular.otf": PROJECT_ROOT / "assets/fonts/Advercase-Regular.otf",
            "/assets/fonts/Advercase-Bold.otf": PROJECT_ROOT / "assets/fonts/Advercase-Bold.otf",
            "/assets/fonts/Anton-Regular.ttf": PROJECT_ROOT / "assets/fonts/Anton-Regular.ttf",
            "/assets/fonts/Axiforma-Regular.ttf": PROJECT_ROOT / "assets/fonts/Axiforma-Regular.ttf",
            "/assets/fonts/Axiforma-SemiBold.ttf": PROJECT_ROOT / "assets/fonts/Axiforma-SemiBold.ttf",
            "/assets/fonts/Axiforma-Black.ttf": PROJECT_ROOT / "assets/fonts/Axiforma-Black.ttf",
            "/assets/brand/editor-carrosseis-logo.png": PROJECT_ROOT / "assets/brand/editor-carrosseis-logo.png",
        }
        if path in safe_assets and safe_assets[path].is_file():
            return self._send_file(safe_assets[path])

        name = Path(urllib.parse.unquote(path)).name
        if name.endswith(".html"):
            target = (EDITOR_DIR / name).resolve()
            if target.parent == EDITOR_DIR.resolve() and target.is_file():
                match = re.fullmatch(ALLOWED_SESSIONS + r"\.html", name)
                if match and hub_session_needs_refresh(target, match.group(1)):
                    refresh_hub_session(target.stem, EDITOR_DIR)
                return self._html(200, _runtime(target.read_text(encoding="utf-8")))
        self.send_error(404)

    def _send_file(self, path: Path) -> None:
        payload = path.read_bytes()
        content_type = "image/png" if path.suffix.lower() == ".png" else "font/otf"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self) -> None:
        if not self._authorized():
            return self._json(403, {"error": "requisição local não autorizada"})
        try:
            if self.path == "/api/sessoes":
                template_id = str(self._read_json().get("template", "")).strip()
                session = create_hub_session(template_id, EDITOR_DIR)
                return self._json(201, {"ok": True, "session_id": session.id, "url": session.url})
            if self.path == "/api/export/pngs":
                return self._export_pngs(self._read_json())
            if self.path in {"/api/gerar-imagem", "/api/salvar-imagem", "/api/publicar-instagram", "/api/telegram/test", "/api/telegram/config", "/api/telegram/send"}:
                return self._json(501, {"error": "integração opcional não configurada neste pacote"})
            return self._json(404, {"error": "rota inexistente"})
        except KeyError as error:
            self._json(400, {"error": "template inválido", "detail": str(error)})
        except (ValueError, json.JSONDecodeError) as error:
            self._json(400, {"error": "payload inválido", "detail": str(error)})

    def _export_pngs(self, body: dict) -> None:
        images = body.get("images_b64") or []
        if not isinstance(images, list) or not images:
            return self._json(400, {"error": "images_b64 deve conter ao menos um PNG"})
        try:
            decoded = [base64.b64decode(str(item).split(",")[-1], validate=True) for item in images]
        except (ValueError, TypeError):
            return self._json(400, {"error": "png inválido"})
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            for index, image in enumerate(decoded, start=1):
                archive.writestr(f"slide-{index:02d}.png", image)
        payload = buffer.getvalue()
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", 'attachment; filename="carrossel-pngs.zip"')
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_DELETE(self) -> None:
        if not self._authorized():
            return self._json(403, {"error": "requisição local não autorizada"})
        match = re.fullmatch(r"/api/sessoes/(" + ALLOWED_SESSIONS + r")", urllib.parse.urlparse(self.path).path)
        if not match:
            return self._json(404, {"error": "sessão inválida"})
        target = EDITOR_DIR / f"{match.group(1)}.html"
        existed = target.is_file()
        target.unlink(missing_ok=True)
        self._json(200, {"ok": True, "deleted": existed})


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("127.0.0.1", PORT), Handler) as server:
        print(f"Editor disponível em http://localhost:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
