"""unique-titles — every slide title should be unique (WCAG / a11y checklists)."""
from __future__ import annotations

from collections import defaultdict
from typing import Any

from ..models import Violation


def _slide_title_text(slide) -> str | None:
    try:
        shapes = slide.shapes
        if getattr(shapes, "title", None) is not None and shapes.title is not None:
            if shapes.title.has_text_frame:
                text = (shapes.title.text_frame.text or "").strip()
                return text or None
    except Exception:
        pass
    # fallback: topmost short text frame
    best: tuple[float, str] | None = None
    for shape in slide.shapes:
        if not getattr(shape, "has_text_frame", False):
            continue
        full = "\n".join(p.text for p in shape.text_frame.paragraphs).strip()
        if not full or len(full) > 120:
            continue
        try:
            top = float(shape.top.pt) if shape.top is not None else 9999.0
        except Exception:
            top = 9999.0
        if best is None or top < best[0]:
            best = (top, full)
    return best[1] if best else None


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    return []


def check_deck(prs, path, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    by_title: dict[str, list[int]] = defaultdict(list)
    missing: list[int] = []
    require_present = bool(rule.get("require_title", True))
    for i, slide in enumerate(prs.slides, start=1):
        title = _slide_title_text(slide)
        if not title:
            if require_present:
                missing.append(i)
            continue
        key = " ".join(title.lower().split())
        by_title[key].append(i)

    out: list[Violation] = []
    sev = rule.get("_severity", "warning")
    for slides in by_title.values():
        if len(slides) < 2:
            continue
        shown = ", ".join(str(s) for s in slides)
        out.append(
            Violation(
                rule_id="unique-titles",
                severity=sev,
                slide=slides[0],
                message_en=f"duplicate slide title on slides {shown}",
                message_zh=f"幻灯片标题重复：第 {shown} 页",
                fix_hint_en="Give each slide a unique, descriptive title for outline/screen-reader navigation.",
                fix_hint_zh="为每页设置唯一且描述性的标题，便于大纲与朗读器导航。",
                category="a11y",
            )
        )
    for i in missing:
        out.append(
            Violation(
                rule_id="unique-titles",
                severity=sev,
                slide=i,
                message_en="slide has no detectable title text",
                message_zh="本页未检测到标题文本",
                fix_hint_en="Add a unique title (placeholder or top text frame).",
                fix_hint_zh="添加唯一标题（标题占位符或顶部文本框）。",
                category="a11y",
            )
        )
    return out
