from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


EDITOR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EDITOR_ROOT))
sys.path.insert(0, str(EDITOR_ROOT / "scripts"))

from editor_core import generate_editor_from_slides  # noqa: E402
from importar_carrossel import load_images, parse_markdown  # noqa: E402
from template_catalog import TEMPLATE_CATALOG  # noqa: E402


class PackageTests(unittest.TestCase):
    def test_catalog_has_only_public_templates(self) -> None:
        self.assertEqual(
            set(TEMPLATE_CATALOG),
            {"tweet", "stories", "stories-fundo", "notes"},
        )

    def test_markdown_import_and_all_templates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "copy.md"
            source.write_text(
                "# Ensaio\n\nSLIDE 1\nGancho.\n\nSLIDE 2\nDesenvolvimento.\n\nSLIDE 3\nConclusão.\n\n## LEGENDA\nLegenda final.",
                encoding="utf-8",
            )
            title, slides, caption = parse_markdown(source)
            self.assertEqual((title, len(slides), caption), ("Ensaio", 3, "Legenda final."))

            for template_id in TEMPLATE_CATALOG:
                output = generate_editor_from_slides(
                    title=title,
                    slides=slides,
                    caption=caption,
                    source_path=source,
                    template_id=template_id,
                    editor_dir=root,
                    output_stem=f"test-{template_id}",
                    profile_name="Marca Teste",
                    handle="marcateste",
                )
                rendered = output.read_text(encoding="utf-8")
                self.assertNotIn("{{", rendered)
                self.assertIn("@marcateste", rendered)
                self.assertIn("Gancho.", rendered)

    def test_local_image_manifest_is_embedded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            image = root / "pixel.png"
            image.write_bytes(
                bytes.fromhex(
                    "89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C489"
                    "0000000D49444154789C6360000000020001E221BC330000000049454E44AE426082"
                )
            )
            manifest = root / "images.json"
            manifest.write_text('{"1": "pixel.png"}', encoding="utf-8")
            images = load_images(manifest, root)
            self.assertTrue(images[1].startswith("data:image/png;base64,"))

    def test_editor_copy_contains_no_private_brand_tokens(self) -> None:
        forbidden = ("anb style", "anb_editor", "academia novo brasil", "omatheus", "matheusão")
        text_files = [
            path
            for pattern in ("*.py", "*.html")
            for path in EDITOR_ROOT.rglob(pattern)
            if "tests" not in path.parts
        ]
        corpus = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in text_files).lower()
        for token in forbidden:
            self.assertNotIn(token, corpus)


if __name__ == "__main__":
    unittest.main()
