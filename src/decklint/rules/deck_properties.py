"""deck-properties — core document title / language (corporate + a11y file QA)."""
from __future__ import annotations

from typing import Any

from ..models import Violation


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    return []


def check_deck(prs, path, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    out: list[Violation] = []
    sev = rule.get("_severity", "warning")
    require_title = bool(rule.get("require_title", True))
    require_language = bool(rule.get("require_language", False))
    title = ""
    language = ""
    try:
        cp = prs.core_properties
        title = (cp.title or "").strip()
        language = (getattr(cp, "language", None) or "").strip()
    except Exception:
        pass
    if require_title and not title:
        out.append(
            Violation(
                rule_id="deck-properties",
                severity=sev,
                slide=None,
                message_en="presentation core property Title is empty",
                message_zh="演示文稿核心属性 Title（标题）为空",
                fix_hint_en="File → Info → Title (or core properties) — set a concise document title.",
                fix_hint_zh="文件 → 信息 → 标题（或核心属性）— 设置简洁的文档标题。",
                category="a11y",
            )
        )
    if require_language and not language:
        out.append(
            Violation(
                rule_id="deck-properties",
                severity=sev,
                slide=None,
                message_en="presentation language metadata is empty",
                message_zh="演示文稿语言元数据为空",
                fix_hint_en="Set document language (Review → Language / core properties).",
                fix_hint_zh="设置文档语言（审阅 → 语言 / 核心属性）。",
                category="a11y",
            )
        )
    return out
