"""font-families — count distinct typefaces; warn if > 3."""
from __future__ import annotations

from typing import Any

from ..models import Violation
from ._shapes import iter_text_runs, run_font_name


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    return []


def check_deck(prs, path, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    names: set[str] = set()
    for slide in prs.slides:
        for shape in slide.shapes:
            for _p, run, text in iter_text_runs(shape):
                if not text.strip():
                    continue
                name = run_font_name(run)
                if name:
                    names.add(name.strip())
    limit = int(rule.get("max", 3))
    if len(names) <= limit:
        return []
    listing = ", ".join(sorted(names))
    return [
        Violation(
            rule_id="font-families",
            severity=rule.get("_severity", "warning"),
            slide=None,
            message_en=f"{len(names)} typefaces (max {limit}): {listing}",
            message_zh=f"{len(names)} 种字体（上限 {limit}）：{listing}",
            fix_hint_en="Stick to ≤3 families (e.g. one display + one body).",
            fix_hint_zh="控制在 ≤3 种字体（例如一种标题 + 一种正文）。",
            category="typography",
        )
    ]
