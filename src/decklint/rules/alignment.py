"""alignment-near-miss — left edges within 2–8pt but not equal."""
from __future__ import annotations

from typing import Any

from ..models import Violation
from ._shapes import shape_box_pt


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    # near-miss band: default 2–8 pt (override via min_delta / max_delta)
    min_delta = float(rule.get("min_delta_pt", 2))
    max_delta = float(rule.get("max_delta_pt", rule.get("tolerance_pt", 8)))
    if max_delta < min_delta:
        max_delta = min_delta + 6

    lefts: list[tuple[str, float]] = []
    for i, shape in enumerate(slide.shapes):
        box = shape_box_pt(shape)
        if not box:
            continue
        # ignore full-bleed backgrounds
        try:
            prs = ctx.get("prs")
            if prs and abs(box[2] - box[0] - prs.slide_width.pt) < 2:
                continue
        except Exception:
            pass
        name = getattr(shape, "name", None) or f"shape{i}"
        lefts.append((name, box[0]))

    out: list[Violation] = []
    for i in range(len(lefts)):
        for j in range(i + 1, len(lefts)):
            a_name, a = lefts[i]
            b_name, b = lefts[j]
            delta = abs(a - b)
            if min_delta <= delta <= max_delta:
                out.append(
                    Violation(
                        rule_id="alignment-near-miss",
                        severity=rule.get("_severity", "warning"),
                        slide=idx,
                        message_en=(
                            f"left edges {delta:.1f}pt apart "
                            f"('{a_name}' vs '{b_name}') — snap to align"
                        ),
                        message_zh=(
                            f"左边距相差 {delta:.1f}pt "
                            f"（「{a_name}」与「{b_name}」）— 应对齐吸附"
                        ),
                        fix_hint_en="Snap left edges to the same guide (CRAP: Alignment).",
                        fix_hint_zh="把左边距吸附到同一参考线（CRAP：对齐）。",
                        category="layout",
                    )
                )
    return out[:5]
