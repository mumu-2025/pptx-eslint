"""box-overlap — axis-aligned overlap of opaque shapes."""
from __future__ import annotations

from typing import Any

from ..models import Violation
from ._shapes import box_area, is_picture, overlap_area, shape_box_pt, shape_solid_fill_rgb


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    threshold = float(rule.get("min_overlap_ratio", 0.15))
    prs = ctx.get("prs")
    slide_area = None
    if prs is not None:
        try:
            slide_area = prs.slide_width.pt * prs.slide_height.pt
        except Exception:
            slide_area = None

    boxes: list[tuple[str, tuple[float, float, float, float]]] = []
    for i, shape in enumerate(slide.shapes):
        opaque = shape_solid_fill_rgb(shape) is not None or is_picture(shape)
        if not opaque:
            continue
        box = shape_box_pt(shape)
        if not box or box_area(box) < 1:
            continue
        # skip full-bleed backgrounds
        if slide_area and box_area(box) / slide_area >= 0.90:
            continue
        name = getattr(shape, "name", None) or f"shape{i}"
        boxes.append((name, box))

    out: list[Violation] = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a_name, a = boxes[i]
            b_name, b = boxes[j]
            ov = overlap_area(a, b)
            if ov <= 0:
                continue
            smaller = min(box_area(a), box_area(b))
            if smaller <= 0:
                continue
            ratio = ov / smaller
            if ratio >= threshold:
                out.append(
                    Violation(
                        rule_id="box-overlap",
                        severity=rule.get("_severity", "warning"),
                        slide=idx,
                        message_en=(
                            f"opaque shapes overlap {ratio:.0%} "
                            f"('{a_name}' × '{b_name}')"
                        ),
                        message_zh=(
                            f"不透明形状重叠 {ratio:.0%} "
                            f"（「{a_name}」×「{b_name}」）"
                        ),
                        fix_hint_en="Separate, stack deliberately, or crop; avoid accidental overlaps.",
                        fix_hint_zh="分开、有意层叠或裁剪；避免无意重叠。",
                        category="layout",
                    )
                )
    return out[:5]
