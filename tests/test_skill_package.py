from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".agents" / "skills" / "social-media-editorial"


class SkillPackageTests(unittest.TestCase):
    def test_skill_is_discoverable_from_project_root(self) -> None:
        self.assertTrue((ROOT / ".agents").is_dir())
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())
        self.assertFalse((ROOT / "projeto-cliente").exists())

    def test_default_editorial_engine_is_present(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        formats = (SKILL_ROOT / "cliente" / "formatos.md").read_text(encoding="utf-8")
        human = (SKILL_ROOT / "references" / "escrita-humanizada.md").read_text(encoding="utf-8")

        for expected in (
            "25 a 45 palavras",
            "40 a 65 palavras",
            "leigo culto",
            "prosa contínua",
            "Filtro Humano",
        ):
            self.assertIn(expected, skill)

        self.assertIn("10 slides", formats)
        self.assertIn("45 a 60", formats)
        self.assertIn("duas frases consecutivas com menos de 10 palavras", human)
        self.assertNotIn("Não imponha três linhas", skill)
        self.assertNotIn("nenhuma linha ou formato ativado", formats)

    def test_skill_markdown_links_resolve(self) -> None:
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        missing: list[str] = []

        for source in SKILL_ROOT.rglob("*.md"):
            for target in pattern.findall(source.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "#")):
                    continue
                target_path = (source.parent / target.split("#", 1)[0]).resolve()
                if not target_path.exists():
                    missing.append(f"{source.relative_to(ROOT)} -> {target}")

        self.assertEqual(missing, [])

    def test_required_references_are_linked_from_entrypoint(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for reference in (
            "references/storytelling.md",
            "references/analise.md",
            "references/noticias.md",
            "references/filtro-humano.md",
            "references/escrita-humanizada.md",
        ):
            self.assertIn(reference, skill)


if __name__ == "__main__":
    unittest.main()
