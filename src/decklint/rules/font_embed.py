"""font-embed — prefer embedded fonts for corporate brand QA (OOXML ppt/fonts)."""
from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from ..models import Violation


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    return []


def check_deck(prs, path, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    path = Path(path)
    require = bool(rule.get("require_embedded", True))
    if not require:
        return []
    has_fonts_part = False
    embed_attr = False
    try:
        with zipfile.ZipFile(path, "r") as zf:
            names = zf.namelist()
            has_fonts_part = any(n.startswith("ppt/fonts/") for n in names)
            if "ppt/presentation.xml" in names:
                root = ET.fromstring(zf.read("ppt/presentation.xml"))
                for el in root.iter():
                    tag = el.tag.rsplit("}", 1)[-1]
                    if tag == "presentation":
                        # embedTrueTypeFonts / saveSubsetFonts often as attributes
                        for k, v in el.attrib.items():
                            lk = k.lower()
                            if "embed" in lk and str(v).lower() in ("1", "true"):
                                embed_attr = True
                    if tag in ("embeddedFontLst", "embeddedFont"):
                        embed_attr = True
    except Exception:
        return []
    if has_fonts_part or embed_attr:
        return []
    return [
        Violation(
            rule_id="font-embed",
            severity=rule.get("_severity", "info"),
            slide=None,
            message_en="no embedded fonts detected in OOXML (ppt/fonts / embed flags)",
            message_zh="OOXML 中未检测到嵌入字体（ppt/fonts / embed 标志）",
            fix_hint_en="File → Options → Save → Embed fonts in the file (corporate brand QA).",
            fix_hint_zh="文件 → 选项 → 保存 → 将字体嵌入文件（企业品牌质检）。",
            category="typography",
        )
    ]
