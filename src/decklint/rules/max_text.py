"""max-text / no-slideument / image layout / title boxes."""
from __future__ import annotations

from typing import Any

from pptx.util import Pt

from ..models import Violation
from ._shapes import is_picture


def check_max_chars(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    texts: list[str] = []
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        full = "\n".join(p.text for p in shape.text_frame.paragraphs).strip()
        if full:
            texts.append(full)
    char_count = sum(len(t) for t in texts)
    limit = int(rule.get("max", 120))
    if char_count <= limit:
        return []
    return [
        Violation(
            rule_id="max-text",
            severity=rule.get("_severity", "error"),
            slide=idx,
            message_en=f"{char_count} characters on slide (max {limit}) — likely a slideument",
            message_zh=f"本页 {char_count} 个字符（上限 {limit}）— 疑似幻灯片文档化",
            fix_hint_en="Cut to one claim + short support; move detail to speaker notes.",
            fix_hint_zh="压缩为一条主张 + 简短支撑；细节放到备注。",
            category="typography",
        )
    ]


def check_bullet_wall(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    bullets = 0
    long_bullets = 0
    max_words = int(rule.get("max_words_per_bullet", 12))
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for p in shape.text_frame.paragraphs:
            text = (p.text or "").strip()
            if not text:
                continue
            is_bullet = bool(getattr(p, "level", 0)) or text.startswith(("•", "-", "·", "–", "*"))
            # also count consecutive body paras as bullets when many
            if is_bullet or (p.level and p.level >= 0 and text.startswith("-")):
                bullets += 1
                if len(text.split()) > max_words:
                    long_bullets += 1
            elif text.startswith("-"):
                bullets += 1
    # recount more liberally: lines starting with dash
    if bullets == 0:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for p in shape.text_frame.paragraphs:
                text = (p.text or "").strip()
                if text.startswith(("-", "•", "·", "*")):
                    bullets += 1
                    if len(text.split()) > max_words:
                        long_bullets += 1

    limit = int(rule.get("max_bullets", 6))
    out: list[Violation] = []
    if bullets > limit:
        out.append(
            Violation(
                rule_id="no-slideument",
                severity=rule.get("_severity", "error"),
                slide=idx,
                message_en=f"{bullets} bullet-like paragraphs (max {limit})",
                message_zh=f"{bullets} 个类项目符号段落（上限 {limit}）",
                fix_hint_en="Turn the list into a visual or a single claim slide.",
                fix_hint_zh="把列表改成可视化或单主张页。",
                category="typography",
            )
        )
    if long_bullets:
        out.append(
            Violation(
                rule_id="no-slideument",
                severity="warning",
                slide=idx,
                message_en=f"{long_bullets} bullet(s) exceed {max_words} words",
                message_zh=f"{long_bullets} 条项目符号超过 {max_words} 词",
                fix_hint_en="Shorten each bullet to a phrase, not a paragraph.",
                fix_hint_zh="把每条压缩成短语，而不是段落。",
                category="typography",
            )
        )
    return out


def check_image_layout(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    images = sum(1 for s in slide.shapes if is_picture(s))
    limit = int(rule.get("max_images", 2))
    if images <= limit:
        return []
    return [
        Violation(
            rule_id="image-bleed",
            severity=rule.get("_severity", "info"),
            slide=idx,
            message_en=f"{images} images — prefer one large visual",
            message_zh=f"{images} 张图片 — 更宜一张大图",
            fix_hint_en="Use one full-bleed or hero image instead of a collage.",
            fix_hint_zh="用一张全出血或主视觉图，而不是拼贴。",
            category="layout",
        )
    ]


def check_title_boxes(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    title_candidates = 0
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        full = "\n".join(p.text for p in shape.text_frame.paragraphs).strip()
        if not full:
            continue
        try:
            if shape.top is not None and shape.top < Pt(120) and len(full) < 80:
                title_candidates += 1
        except Exception:
            pass
    limit = int(rule.get("max", 1))
    if title_candidates <= limit + 2:
        return []
    return [
        Violation(
            rule_id="one-idea",
            severity=rule.get("_severity", "error"),
            slide=idx,
            message_en=f"{title_candidates} top text frames — possible multi-idea slide",
            message_zh=f"顶部有 {title_candidates} 个文本框 — 可能一页多主张",
            fix_hint_en="Split into one idea per slide.",
            fix_hint_zh="拆成一页一个主张。",
            category="design",
        )
    ]
