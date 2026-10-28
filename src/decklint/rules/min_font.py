"""min-font — scan run font sizes; respect preset floors."""
from __future__ import annotations

from typing import Any

from ..models import Violation
from ._shapes import iter_text_runs, run_font_size_pt


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    sizes: list[float] = []
    for shape in slide.shapes:
        for _p, run, text in iter_text_runs(shape):
            if not text.strip():
                continue
            pt = run_font_size_pt(run)
            if pt is not None:
                sizes.append(pt)
    if not sizes:
        return []
    floor = float(rule.get("min", 18))
    smallest = min(sizes)
    if smallest >= floor:
        return []
    return [
        Violation(
            rule_id="min-font",
            severity=rule.get("_severity", "error"),
            slide=idx,
            message_en=f"smallest font {smallest:.0f}pt < {floor:.0f}pt",
            message_zh=f"最小字号 {smallest:.0f}pt < {floor:.0f}pt",
            fix_hint_en="Raise body text to the preset floor; move dense text to notes.",
            fix_hint_zh="把正文字号提到预设下限；密集文字移到备注。",
            category="typography",
        )
    ]
