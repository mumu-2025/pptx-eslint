"""max-shapes — too many shapes usually means visual clutter."""
from __future__ import annotations

from typing import Any

from ..models import Violation
from ._shapes import shape_box_pt, slide_size_inches


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    limit = int(rule.get("max", 25))
    prs = ctx.get("prs")
    slide_area = 0.0
    if prs is not None:
        w, h = slide_size_inches(prs)
        slide_area = w * 72.0 * h * 72.0
    count = 0
    for shape in slide.shapes:
        box = shape_box_pt(shape)
        if box is None:
            count += 1
            continue
        l, t, r, b = box
        area = max(0.0, (r - l) * (b - t))
        # ignore full-bleed backgrounds
        if slide_area > 0 and area / slide_area >= 0.92:
            continue
        count += 1
    if count <= limit:
        return []
    return [
        Violation(
            rule_id="max-shapes",
            severity=rule.get("_severity", "warning"),
            slide=idx,
            message_en=f"{count} shapes on slide (max {limit}) — likely clutter",
            message_zh=f"本页有 {count} 个形状（上限 {limit}）— 可能过于拥挤",
            fix_hint_en="Simplify: group, remove decoration, or split across slides.",
            fix_hint_zh="简化：合并、去掉装饰，或拆到多页。",
            category="layout",
        )
    ]
