"""vague-links — ban non-descriptive hyperlink labels (a11y checklists)."""
from __future__ import annotations

from typing import Any

from ..models import Violation

DEFAULT_BANNED = (
    "click here",
    "click here.",
    "here",
    "learn more",
    "read more",
    "more",
    "link",
    "this link",
    "点击这里",
    "点这里",
    "点击此处",
    "了解更多",
    "详见",
    "更多",
)


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    banned = [b.lower() for b in (rule.get("ban_phrases") or DEFAULT_BANNED)]
    hits: list[str] = []
    for shape in slide.shapes:
        if not getattr(shape, "has_text_frame", False):
            continue
        for p in shape.text_frame.paragraphs:
            for run in p.runs:
                text = (run.text or "").strip()
                if not text:
                    continue
                has_link = False
                try:
                    hl = run.hyperlink
                    if hl is not None and (hl.address or getattr(hl, "_hlink", None)):
                        has_link = True
                except Exception:
                    has_link = False
                # also detect OOXML hlinkClick via element
                if not has_link:
                    try:
                        el = run._r  # noqa: SLF001
                        blob = el.xml if hasattr(el, "xml") else str(el)
                        if "hlinkClick" in blob or "hyperlink" in blob.lower():
                            has_link = True
                    except Exception:
                        pass
                if not has_link:
                    continue
                low = text.lower()
                if low in banned or any(low == b for b in banned):
                    hits.append(text)
    if not hits:
        return []
    sample = ", ".join(repr(h) for h in hits[:5])
    return [
        Violation(
            rule_id="vague-links",
            severity=rule.get("_severity", "warning"),
            slide=idx,
            message_en=f"vague hyperlink label(s): {sample}",
            message_zh=f"含糊的超链接文案：{sample}",
            fix_hint_en='Use descriptive link text (destination/purpose), not "click here" / "了解更多".',
            fix_hint_zh="使用描述目的/去向的链接文案，避免「点击这里」「了解更多」。",
            category="a11y",
        )
    ]
