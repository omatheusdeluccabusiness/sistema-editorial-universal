#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import webbrowser
from pathlib import Path

try:
    from scripts.editor_core import generate_editor_from_slides, slugify
    from scripts.template_catalog import TEMPLATE_CATALOG
except ImportError:
    from editor_core import generate_editor_from_slides, slugify
    from template_catalog import TEMPLATE_CATALOG


ROOT = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("CARROSSEL_EDITOR_PORT", "8797"))
EDITOR_DIR = Path(os.environ.get("CARROSSEL_EDITOR_DIR", str(Path(tempfile.gettempdir()) / "carrossel-editor-universal")))
SERVICE = ROOT / "scripts" / "carrossel_service.py"


def parse_markdown(path: Path) -> tuple[str, list[str], str]:
    text = path.read_text(encoding="utf-8-sig")
    title_match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    title = title_match.group(1).strip() if title_match else path.stem
    caption_match = re.search(r"(?ims)^#{1,3}\s+(?:legenda|caption)(?:\s+instagram)?\s*$\s*(.+?)(?=^#{1,3}\s|\Z)", text)
    caption = caption_match.group(1).strip() if caption_match else ""

    slide_pattern = re.compile(
        r"(?ims)^(?:#{1,4}\s*)?(?:slide|card)\s*0*(\d{1,2})(?:\s*[-—:]\s*[^\n]*)?\s*$\s*(.+?)(?=^(?:#{1,4}\s*)?(?:slide|card)\s*0*\d{1,2}(?:\s*[-—:]\s*[^\n]*)?\s*$|^#{1,3}\s+(?:legenda|caption)(?:\s+instagram)?\s*$|\Z)"
    )
    found = [(int(match.group(1)), match.group(2).strip()) for match in slide_pattern.finditer(text)]
    if not found:
        raise ValueError("Nenhum bloco 'SLIDE N' foi encontrado no Markdown.")
    found.sort(key=lambda item: item[0])
    expected = list(range(1, len(found) + 1))
    actual = [number for number, _ in found]
    if actual != expected:
        raise ValueError(f"Os slides devem ser consecutivos a partir de 1. Recebido: {actual}")
    return title, [copy for _, copy in found], caption


def _data_url(source: str, base_dir: Path) -> str:
    parsed = source.strip()
    if parsed.startswith("data:image/"):
        return parsed
    if re.match(r"^https?://", parsed, re.I):
        request = urllib.request.Request(parsed, headers={"User-Agent": "Mozilla/5.0 CarouselEditorUniversal/1.1"})
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read(15 * 1024 * 1024 + 1)
            content_type = response.headers.get_content_type()
    else:
        path = Path(parsed)
        if not path.is_absolute():
            path = base_dir / path
        payload = path.resolve().read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    if len(payload) > 15 * 1024 * 1024:
        raise ValueError(f"Imagem maior que 15 MB: {source}")
    if not content_type.startswith("image/"):
        raise ValueError(f"O arquivo não parece ser uma imagem: {source}")
    return f"data:{content_type};base64," + base64.b64encode(payload).decode("ascii")


def load_images(manifest_path: Path | None, base_dir: Path) -> dict[int, str]:
    if not manifest_path:
        return {}
    raw = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if not isinstance(raw, dict):
        raise ValueError("O manifesto de imagens deve ser um objeto JSON.")
    result = {}
    for key, value in raw.items():
        number = int(str(key).lower().replace("slide", "").strip())
        if number < 1 or not isinstance(value, str) or not value.strip():
            raise ValueError(f"Entrada de imagem inválida: {key}")
        result[number] = _data_url(value, base_dir)
    return result


def server_ready() -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/api/health", timeout=0.7) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload.get("ok") is True and payload.get("service") == "editor-carrosseis-universal"
    except (OSError, ValueError, json.JSONDecodeError):
        return False


def port_open() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=0.4):
            return True
    except OSError:
        return False


def ensure_server() -> None:
    if server_ready():
        return
    if port_open():
        raise RuntimeError(f"A porta {PORT} está ocupada por outro programa. Defina CARROSSEL_EDITOR_PORT para usar outra porta.")
    completed = subprocess.run([sys.executable, str(SERVICE), "start"], capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError((completed.stderr or completed.stdout or "O servidor não iniciou.").strip())
    for _ in range(30):
        if server_ready():
            return
        time.sleep(0.2)
    raise RuntimeError("O servidor não respondeu na porta 8797.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Importa uma copy aprovada no editor de carrosséis.")
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--template", choices=sorted(TEMPLATE_CATALOG), required=True)
    parser.add_argument("--images", type=Path, help="JSON opcional: número do slide para URL ou arquivo de imagem.")
    parser.add_argument("--title", help="Sobrescreve o título do Markdown.")
    parser.add_argument("--caption", help="Sobrescreve a legenda do Markdown.")
    parser.add_argument("--profile-name", default="Seu Perfil", help="Nome exibido no template.")
    parser.add_argument("--handle", default="seuperfil", help="Arroba exibido, com ou sem @.")
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()

    markdown = args.markdown.expanduser().resolve()
    title, slides, caption = parse_markdown(markdown)
    images = load_images(args.images.expanduser().resolve() if args.images else None, markdown.parent)
    output = generate_editor_from_slides(
        title=args.title or title,
        slides=slides,
        caption=args.caption if args.caption is not None else caption,
        source_path=markdown,
        template_id=args.template,
        editor_dir=EDITOR_DIR,
        image_data_urls=images,
        output_stem=f"{slugify(args.title or title)}-{args.template}-{time.time_ns()}",
        profile_name=args.profile_name,
        handle=args.handle,
    )
    ensure_server()
    url = f"http://localhost:{PORT}/{output.name}"
    if not args.no_open:
        webbrowser.open(url)
    print(json.dumps({
        "ok": True,
        "template": args.template,
        "slides": len(slides),
        "images": len(images),
        "html": str(output),
        "url": url,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
