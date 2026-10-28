"""safe-margins — content should stay inside outer safe area (Duarte grid margins)."""
from __future__ import annotations

from typing import Any

from ..models import Violation
from ._shapes import is_picture, shape_box_pt, slide_size_inches


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    prs = ctx.get("prs")
    if prs is None:
        return []
    w_in, h_in = slide_size_inches(prs)
    w_pt = w_in * 72.0
    h_pt = h_in * 72.0
    margin_pct = float(rule.get("margin_pct", 0.05))
    allow_bleed = bool(rule.get("allow_full_bleed_images", True))
    mx = w_pt * margin_pct
    my = h_pt * margin_pct
    # ignore full-bleed backgrounds: shapes covering ≥92% of slide
    slide_area = w_pt * h_pt
    violators = 0
    for shape in slide.shapes:
        box = shape_box_pt(shape)
        if box is None:
            continue
        l, t, r, b = box
        area = max(0.0, (r - l) * (b - t))
        if slide_area > 0 and area / slide_area >= 0.92:
            continue  # full-bleed bg / hero
        if allow_bleed and is_picture(shape) and slide_area > 0 and area / slide_area >= 0.85:
            continue
        # near-edge intrusion (outside safe inset)
        if l < mx - 0.5 or t < my - 0.5 or r > w_pt - mx + 0.5 or b > h_pt - my + 0.5:
            violators += 1
    if violators == 0:
        return []
    pct = int(round(margin_pct * 100))
    return [
        Violation(
            rule_id="safe-margins",
            severity=rule.get("_severity", "warning"),
            slide=idx,
            message_en=f"{violators} shape(s) intrude into ~{pct}% outer margin",
            message_zh=f"{violators} 个形状侵入约 {pct}% 外边距安全区",
            fix_hint_en="Keep content inside outer margins (~5% of width/height) unless intentionally full-bleed.",
            fix_hint_zh="除非有意全出血，内容应留在外边距内（约宽高的 5%）。",
            category="layout",
        )
    ]
