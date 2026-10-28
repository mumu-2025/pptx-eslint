"""image-alt / a11y-title — accessibility heuristics."""
from __future__ import annotations

from typing import Any

from ..models import Violation
from ._shapes import is_picture, picture_descr, slide_has_title


def check_image_alt(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    out: list[Violation] = []
    for shape in slide.shapes:
        if not is_picture(shape):
            continue
        descr = picture_descr(shape)
        name = (getattr(shape, "name", None) or "").strip()
        # missing meaningful alt: no descr, or generic "Picture *"
        generic = not descr and (not name or name.lower().startswith("picture"))
        if descr:
            continue
        if generic or not descr:
            out.append(
                Violation(
                    rule_id="image-alt",
                    severity=rule.get("_severity", "warning"),
                    slide=idx,
                    message_en=f"picture '{name or '?'}' missing descr/alt text",
                    message_zh=f"图片「{name or '?'}」缺少 descr/替代文本",
                    fix_hint_en="Set alternative text (descr) describing the image purpose.",
                    fix_hint_zh="设置描述图片用途的替代文本（descr）。",
                    category="a11y",
                )
            )
    return out


def check_a11y_title(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    # Best-effort: if layout name suggests a titled layout, require title placeholder text
    layout_name = ""
    try:
        layout_name = (slide.slide_layout.name or "").lower()
    except Exception:
        layout_name = ""
    titled_hints = ("title", "标题", "section", "agenda", "name card")
    looks_titled = any(h in layout_name for h in titled_hints)
    # blank layout (often index 6) — skip
    if "blank" in layout_name or "空白" in layout_name:
        return []
    if not looks_titled:
        # still flag completely empty of any top text when using non-blank? soft skip
        return []
    if slide_has_title(slide):
        return []
    return [
        Violation(
            rule_id="a11y-title",
            severity=rule.get("_severity", "warning"),
            slide=idx,
            message_en=f"layout '{layout_name}' expects a title placeholder",
            message_zh=f"版式「{layout_name}」应有标题占位内容",
            fix_hint_en="Fill the title placeholder for screen-reader / outline navigation.",
            fix_hint_zh="填写标题占位符，便于朗读器与大纲导航。",
            category="a11y",
        )
    ]
