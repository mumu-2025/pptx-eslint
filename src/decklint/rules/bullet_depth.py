"""bullet-depth — limit nested bullet levels (readability / a11y)."""
from __future__ import annotations

from typing import Any

from ..models import Violation


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    max_level = int(rule.get("max_level", 2))  # 0-based: 0,1,2 → three levels
    deepest = -1
    deep_count = 0
    for shape in slide.shapes:
        if not getattr(shape, "has_text_frame", False):
            continue
        for p in shape.text_frame.paragraphs:
            text = (p.text or "").strip()
            if not text:
                continue
            try:
                level = int(p.level or 0)
            except Exception:
                level = 0
            if level > deepest:
                deepest = level
            if level > max_level:
                deep_count += 1
    if deep_count == 0:
        return []
    return [
        Violation(
            rule_id="bullet-depth",
            severity=rule.get("_severity", "warning"),
            slide=idx,
            message_en=f"{deep_count} paragraph(s) nest deeper than level {max_level} (deepest={deepest})",
            message_zh=f"{deep_count} 个段落嵌套超过第 {max_level} 级（最深={deepest}）",
            fix_hint_en="Flatten lists; prefer ≤3 nesting levels (0–2) for projected reading.",
            fix_hint_zh="压平列表；投影阅读建议不超过 3 层嵌套（0–2 级）。",
            category="typography",
        )
    ]
