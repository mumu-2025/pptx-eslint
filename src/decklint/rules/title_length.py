"""title-length — titles should be scannable (not empty stubs, not paragraphs)."""
from __future__ import annotations

from typing import Any

from ..models import Violation
from .unique_titles import _slide_title_text


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    title = _slide_title_text(slide)
    if not title:
        return []
    min_c = int(rule.get("min_chars", 4))
    max_c = int(rule.get("max_chars", 90))
    n = len(title)
    out: list[Violation] = []
    sev = rule.get("_severity", "info")
    if n < min_c:
        out.append(
            Violation(
                rule_id="title-length",
                severity=sev,
                slide=idx,
                message_en=f"title too short ({n} chars, min {min_c}): {title!r}",
                message_zh=f"标题过短（{n} 字符，最少 {min_c}）：{title!r}",
                fix_hint_en="Use a scannable claim, not a one-letter stub.",
                fix_hint_zh="使用可扫读的主张，而不是单字占位。",
                category="design",
            )
        )
    if n > max_c:
        out.append(
            Violation(
                rule_id="title-length",
                severity=sev,
                slide=idx,
                message_en=f"title too long ({n} chars, max {max_c})",
                message_zh=f"标题过长（{n} 字符，上限 {max_c}）",
                fix_hint_en="Shorten the title; move detail into body or notes.",
                fix_hint_zh="缩短标题；细节放到正文或备注。",
                category="design",
            )
        )
    return out
