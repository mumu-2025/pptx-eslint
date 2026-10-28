"""canvas — warn if not ~16:9; info if 4:3 legacy."""
from __future__ import annotations

from typing import Any

from ..models import Violation
from ._shapes import slide_size_inches


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    return []


def check_deck(prs, path, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    w, h = slide_size_inches(prs)
    if h <= 0:
        return []
    ratio = w / h
    # 16:9 ≈ 1.777; standard 13.333×7.5
    widescreen = abs(ratio - 16 / 9) < 0.05 or (
        abs(w - 13.333) < 0.05 and abs(h - 7.5) < 0.05
    )
    legacy_43 = abs(ratio - 4 / 3) < 0.05
    if widescreen:
        return []
    if legacy_43:
        return [
            Violation(
                rule_id="canvas",
                severity="info",
                slide=None,
                message_en=f"legacy 4:3 canvas ({w:.2f}×{h:.2f}\") — prefer 16:9",
                message_zh=f"遗留 4:3 画布（{w:.2f}×{h:.2f}\"）— 建议改用 16:9",
                fix_hint_en="Switch slide size to 13.333×7.5 in (widescreen).",
                fix_hint_zh="将幻灯片大小改为 13.333×7.5 英寸（宽屏）。",
                category="design",
            )
        ]
    return [
        Violation(
            rule_id="canvas",
            severity=rule.get("_severity", "warning"),
            slide=None,
            message_en=f"canvas {w:.2f}×{h:.2f}\" (ratio {ratio:.3f}) is not ~16:9",
            message_zh=f"画布 {w:.2f}×{h:.2f}\"（比例 {ratio:.3f}）不是约 16:9",
            fix_hint_en="Use widescreen 16:9 (13.333×7.5\") unless a venue requires otherwise.",
            fix_hint_zh="除非场地另有要求，请使用 16:9 宽屏（13.333×7.5\"）。",
            category="design",
        )
    ]
