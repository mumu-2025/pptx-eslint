"""empty-slide — flag slides with no meaningful content."""
from __future__ import annotations

from typing import Any

from pptx.enum.shapes import MSO_SHAPE_TYPE

from ..models import Violation
from ._shapes import is_picture


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    min_chars = int(rule.get("min_chars", 1))
    allow_picture_only = bool(rule.get("allow_picture_only", True))
    chars = 0
    pics = 0
    charts = 0
    other = 0
    for shape in slide.shapes:
        if getattr(shape, "has_text_frame", False):
            for p in shape.text_frame.paragraphs:
                chars += len((p.text or "").strip())
        if is_picture(shape):
            pics += 1
            continue
        try:
            st = shape.shape_type
            if st == MSO_SHAPE_TYPE.CHART:
                charts += 1
                continue
            if st == MSO_SHAPE_TYPE.TABLE:
                other += 1
                continue
            if st == MSO_SHAPE_TYPE.GROUP:
                other += 1
                continue
            # skip near full-bleed rectangles used as backgrounds
            if st == MSO_SHAPE_TYPE.AUTO_SHAPE:
                try:
                    if shape.width and shape.height:
                        # count as content only if not huge fill
                        other += 1
                except Exception:
                    other += 1
        except Exception:
            other += 1
    if chars >= min_chars:
        return []
    if allow_picture_only and pics > 0:
        return []
    if charts > 0 or other > 2:
        return []
    if pics == 0 and charts == 0 and chars < min_chars:
        return [
            Violation(
                rule_id="empty-slide",
                severity=rule.get("_severity", "info"),
                slide=idx,
                message_en="slide appears empty (no text / picture / chart)",
                message_zh="本页疑似空白（无文本 / 图片 / 图表）",
                fix_hint_en="Remove the blank slide or add a title/claim.",
                fix_hint_zh="删除空白页，或补充标题/主张。",
                category="design",
            )
        ]
    return []
