"""accent-colors — distinct non-near-gray RGB from fonts/fills."""
from __future__ import annotations

from typing import Any

from ..contrast import is_near_gray
from ..models import Violation
from ._shapes import (
    iter_text_runs,
    run_font_rgb,
    shape_solid_fill_rgb,
)


def _collect_accents(prs) -> set[tuple[int, int, int]]:
    accents: set[tuple[int, int, int]] = set()
    for slide in prs.slides:
        for shape in slide.shapes:
            fill = shape_solid_fill_rgb(shape)
            if fill and not is_near_gray(fill):
                accents.add(_quantize(fill))
            for _p, run, text in iter_text_runs(shape):
                if not text.strip():
                    continue
                fg = run_font_rgb(run)
                if fg and not is_near_gray(fg):
                    accents.add(_quantize(fg))
    return accents


def _quantize(rgb: tuple[int, int, int], step: int = 16) -> tuple[int, int, int]:
    return tuple((c // step) * step for c in rgb)  # type: ignore[return-value]


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    # per-slide collection is informational; deck-level does the warn
    return []


def check_deck(prs, path, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    accents = _collect_accents(prs)
    limit = int(rule.get("max", 2))
    if len(accents) <= limit:
        return []
    sample = ", ".join(f"#{r:02X}{g:02X}{b:02X}" for r, g, b in sorted(accents)[:8])
    return [
        Violation(
            rule_id="accent-colors",
            severity=rule.get("_severity", "warning"),
            slide=None,
            message_en=f"{len(accents)} distinct accent colors (max {limit}): {sample}",
            message_zh=f"{len(accents)} 种强调色（上限 {limit}）：{sample}",
            fix_hint_en="Reduce to 1–2 purposeful accent colors (Duarte).",
            fix_hint_zh="收敛到 1–2 种有目的的强调色（Duarte）。",
            category="color",
        )
    ]
