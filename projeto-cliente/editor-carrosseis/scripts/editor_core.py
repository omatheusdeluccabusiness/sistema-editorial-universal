from __future__ import annotations

import hashlib
import html
import json
import re
import unicodedata
from pathlib import Path

try:
    from scripts.template_catalog import get_template
except ImportError:
    from template_catalog import get_template


DEFAULT_COPY = "Adicione aqui a sua copy."


def slugify(value: str) -> str:
    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_-]+", "-", text)[:60] or "carrossel"


def _inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", escaped)


def _slide_html(number: int, total: int, text: str, image_data_url: str | None) -> str:
    if number == 1:
        kind, label, background = "capa", "Capa", "bg-01"
    elif number == total:
        kind, label, background = "cta", "CTA final", "bg-10"
    else:
        kind, label = "corpo", f"Slide {number}"
        backgrounds = ["bg-03", "bg-04", "bg-05", "bg-06", "bg-07", "bg-08", "bg-09"]
        background = backgrounds[(number - 2) % len(backgrounds)]

    blocks = []
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    for index, paragraph in enumerate(paragraphs):
        if kind == "capa":
            variant = "big"
        elif kind == "cta":
            variant = "big"
        elif paragraph.startswith("(") and paragraph.endswith(")"):
            variant = "italic"
        elif index > 0 and len(paragraph) < 100:
            variant = "lede"
        else:
            variant = "lede"
        blocks.append(f'<div class="body {variant}">{_inline(paragraph)}</div>')

    photo_style = ""
    if image_data_url:
        photo_style = f' style="background-image:url(&quot;{html.escape(image_data_url, quote=True)}&quot;)"'
    joined = "\n".join("          " + block for block in blocks)
    extra_class = " capa" if kind == "capa" else " cta-final" if kind == "cta" else ""
    return f'''  <!-- ===== SLIDE {number:02d} — {label} ===== -->
  <div class="slide-wrap">
    <div class="slide-label">{number:02d} — {label}</div>
    <div class="stage">
      <div class="slide {background}{extra_class}" data-fade="1.0">
        <div class="photo"{photo_style}></div>
        <div class="body-zone">
{joined}
        </div>
        <div class="footer-bar" style="display:flex;justify-content:space-between;">
          <div class="footer-tag">@seuperfil</div>
          <div class="footer-tag" style="text-align:right;">{number:02d} / {total:02d}</div>
        </div>
      </div>
    </div>
  </div>'''


def _render_template(
    *,
    title: str,
    slides: list[str],
    caption: str,
    template_id: str,
    source_key: str,
    image_data_urls: dict[int, str] | None,
    hub_session: bool,
    hub_session_id: str,
    profile_name: str,
    handle: str,
) -> str:
    definition = get_template(template_id)
    template = definition.template_path.read_text(encoding="utf-8")
    images = image_data_urls or {}
    slide_json = []
    slide_html = []
    total = len(slides)
    for index, copy in enumerate(slides, start=1):
        label = f"{index} — " + ("Capa" if index == 1 else "CTA" if index == total else "Slide")
        slide_json.append({"label": label, "text": copy, "imageDataURL": images.get(index)})
        slide_html.append(_slide_html(index, total, copy, images.get(index)))

    digest = hashlib.sha256(json.dumps(slide_json, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]
    doc_key = f"carrossel-editor-{slugify(source_key)}-universal-v1-{digest}"
    replacements = {
        "{{TITLE}}": html.escape(title),
        "{{N_SLIDES}}": str(total),
        "{{CAPTION}}": html.escape(caption),
        "{{SLIDES_JSON}}": json.dumps(slide_json, ensure_ascii=False),
        "{{SLIDES_HTML}}": "\n\n".join(slide_html),
        "{{DOC_KEY}}": doc_key,
        "{{PECA_PATH}}": "",
        "{{HUB_SESSION}}": "true" if hub_session else "false",
        "{{HUB_SESSION_ID}}": hub_session_id,
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    clean_handle = handle.strip().lstrip("@") or "seuperfil"
    template = template.replace("Seu Perfil", profile_name.strip() or "Seu Perfil")
    template = template.replace("@seuperfil", "@" + clean_handle)
    template = template.replace("'seuperfil'", repr(clean_handle))
    return template


def generate_editor_from_slides(
    *,
    title: str,
    slides: list[str],
    caption: str,
    source_path: Path,
    template_id: str,
    editor_dir: Path,
    image_data_urls: dict[int, str] | None = None,
    output_stem: str | None = None,
    hub_session: bool = False,
    profile_name: str = "Seu Perfil",
    handle: str = "seuperfil",
) -> Path:
    definition = get_template(template_id)
    if not 2 <= len(slides) <= definition.initial_slides:
        raise ValueError(f"O template {template_id} aceita de 2 a {definition.initial_slides} slides.")
    if any(not isinstance(text, str) or not text.strip() for text in slides):
        raise ValueError("Todos os slides precisam conter texto.")

    stem = output_stem or slugify(title)
    rendered = _render_template(
        title=title.strip() or source_path.stem,
        slides=[text.strip() for text in slides],
        caption=caption.strip(),
        template_id=template_id,
        source_key=str(source_path.resolve()),
        image_data_urls=image_data_urls,
        hub_session=hub_session,
        hub_session_id=stem if hub_session else "",
        profile_name=profile_name,
        handle=handle,
    )
    editor_dir.mkdir(parents=True, exist_ok=True)
    output = editor_dir / f"{stem}.html"
    output.write_text(rendered, encoding="utf-8")
    return output


def generate_blank_editor(
    *,
    title: str,
    template_id: str,
    editor_dir: Path,
    output_stem: str,
    hub_session: bool,
) -> Path:
    definition = get_template(template_id)
    source = editor_dir / f"{output_stem}.md"
    return generate_editor_from_slides(
        title=title,
        slides=[DEFAULT_COPY] * definition.initial_slides,
        caption="Adicione aqui a legenda.",
        source_path=source,
        template_id=template_id,
        editor_dir=editor_dir,
        output_stem=output_stem,
        hub_session=hub_session,
        profile_name="Seu Perfil",
        handle="seuperfil",
    )
