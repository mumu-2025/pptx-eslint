"""auto-advance — flag timed slide advances (WCAG / user-control)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..models import Violation
from ..ooxml import parse_auto_advances


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    return []


def check_deck(prs, path, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    path = Path(path)
    try:
        hits = parse_auto_advances(path)
    except Exception:
        return []
    if not hits:
        return []
    out: list[Violation] = []
    sev = rule.get("_severity", "warning")
    for h in hits:
        out.append(
            Violation(
                rule_id="auto-advance",
                severity=sev,
                slide=h.get("slide"),
                message_en=f"timed auto-advance ({h.get('adv_ms')} ms) — prefer on-click",
                message_zh=f"定时自动进片（{h.get('adv_ms')} ms）— 建议改为单击进片",
                fix_hint_en="Transitions → Advance Slide → On Mouse Click (uncheck After).",
                fix_hint_zh="切换 → 换片方式 → 单击鼠标时（取消勾选「在此之后」）。",
                category="a11y",
            )
        )
    return out
