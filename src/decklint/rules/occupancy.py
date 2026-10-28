"""occupancy — sum shape areas / slide area; warn if > threshold."""
from __future__ import annotations

from typing import Any

from ..models import Violation
from ._shapes import box_area, shape_box_pt


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    prs = ctx.get("prs")
    if prs is None:
        return []
    try:
        sw = prs.slide_width.pt
        sh = prs.slide_height.pt
        slide_area = sw * sh
    except Exception:
        return []
    if slide_area <= 0:
        return []
    total = 0.0
    for shape in slide.shapes:
        box = shape_box_pt(shape)
        if not box:
            continue
        area = box_area(box)
        # Skip near-full-bleed backgrounds (decorative canvas fills)
        if area / slide_area >= 0.90:
            continue
        total += area
    ratio = total / slide_area
    limit = float(rule.get("max_fill_ratio", 0.72))
    if ratio <= limit:
        return []
    return [
        Violation(
            rule_id="occupancy",
            severity=rule.get("_severity", "warning"),
            slide=idx,
            message_en=f"shape occupancy {ratio:.0%} > {limit:.0%}",
            message_zh=f"形状占版率 {ratio:.0%} > {limit:.0%}",
            fix_hint_en="Leave whitespace; remove or shrink non-essential boxes.",
            fix_hint_zh="留白；删除或缩小非必要框。",
            category="layout",
        )
    ]
