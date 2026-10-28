"""Pluggable rule checkers. Each returns list[Violation]."""
from __future__ import annotations

from typing import Any, Callable

from pptx.slide import Slide

from ..models import Violation
from . import (
    accent_colors,
    alignment,
    animation_policy,
    box_overlap,
    canvas,
    chart_junk,
    font_families,
    image_alt,
    max_text,
    min_font,
    occupancy,
    text_contrast,
    title_as_claim,
)

CheckFn = Callable[[Slide, int, dict[str, Any], dict[str, Any]], list[Violation]]

# Map YAML `check` key → callable
CHECKERS: dict[str, CheckFn] = {
    "max_chars_per_slide": max_text.check_max_chars,
    "bullet_wall": max_text.check_bullet_wall,
    "min_font_pt": min_font.check,
    "text_bg_contrast": text_contrast.check,
    "max_accent_colors": accent_colors.check,
    "font_families": font_families.check,
    "box_overlap": box_overlap.check,
    "canvas_ratio": canvas.check,
    "title_is_claim": title_as_claim.check,
    "chart_junk": chart_junk.check,
    "animation_policy": animation_policy.check,
    "image_alt": image_alt.check_image_alt,
    "a11y_title": image_alt.check_a11y_title,
    "occupancy": occupancy.check,
    "near_miss_alignment": alignment.check,
    "image_layout": max_text.check_image_layout,
    "max_title_boxes": max_text.check_title_boxes,
}

# Deck-level checkers (run once with presentation + path context)
DECK_CHECKERS: dict[str, Callable[..., list[Violation]]] = {
    "canvas_ratio": canvas.check_deck,
    "max_accent_colors": accent_colors.check_deck,
    "font_families": font_families.check_deck,
    "animation_policy": animation_policy.check_deck,
}

RULE_DOCS: list[dict[str, str]] = [
    {
        "id": "max-text",
        "check": "max_chars_per_slide",
        "category": "typography",
        "en": "Limit characters per slide (anti-slideument).",
        "zh": "限制每页字符数（反幻灯片文档化）。",
    },
    {
        "id": "no-slideument",
        "check": "bullet_wall",
        "category": "typography",
        "en": "Flag wall-of-bullets slides.",
        "zh": "标记子弹墙幻灯片。",
    },
    {
        "id": "min-font",
        "check": "min_font_pt",
        "category": "typography",
        "en": "Enforce minimum font size for the back of the room.",
        "zh": "强制最小字号，保证后排可读。",
    },
    {
        "id": "text-contrast",
        "check": "text_bg_contrast",
        "category": "a11y",
        "en": "WCAG contrast between text RGB and solid fill.",
        "zh": "文本 RGB 与纯色填充的 WCAG 对比度。",
    },
    {
        "id": "accent-colors",
        "check": "max_accent_colors",
        "category": "color",
        "en": "Limit distinct non-near-gray accent colors.",
        "zh": "限制非近灰强调色数量。",
    },
    {
        "id": "font-families",
        "check": "font_families",
        "category": "typography",
        "en": "Warn if more than 3 distinct typefaces.",
        "zh": "超过 3 种字体则警告。",
    },
    {
        "id": "box-overlap",
        "check": "box_overlap",
        "category": "layout",
        "en": "Axis-aligned overlap of opaque shapes.",
        "zh": "不透明形状轴对齐重叠检测。",
    },
    {
        "id": "canvas",
        "check": "canvas_ratio",
        "category": "design",
        "en": "Prefer ~16:9 widescreen; info for 4:3 legacy.",
        "zh": "优先约 16:9 宽屏；4:3 遗留比例提示。",
    },
    {
        "id": "title-as-claim",
        "check": "title_is_claim",
        "category": "design",
        "en": "Ban vague titles (Overview / 概况 / 目录 …).",
        "zh": "禁止空泛标题（Overview / 概况 / 目录 …）。",
    },
    {
        "id": "chart-junk",
        "check": "chart_junk",
        "category": "chart",
        "en": "Flag 3D-ish charts; remind to add callouts.",
        "zh": "标记疑似 3D 图表；提醒添加标注。",
    },
    {
        "id": "animation-policy",
        "check": "animation_policy",
        "category": "animation",
        "en": "Ban decorative animations; cap transition variety.",
        "zh": "禁止装饰性动画；限制切换效果种类。",
    },
    {
        "id": "image-alt",
        "check": "image_alt",
        "category": "a11y",
        "en": "Pictures missing descr / alt text.",
        "zh": "图片缺少 descr / 替代文本。",
    },
    {
        "id": "a11y-title",
        "check": "a11y_title",
        "category": "a11y",
        "en": "Titled layouts should expose a title placeholder.",
        "zh": "带标题版式应提供标题占位符。",
    },
    {
        "id": "occupancy",
        "check": "occupancy",
        "category": "layout",
        "en": "Warn if shape area / slide area > 0.72.",
        "zh": "形状总面积 / 幻灯片面积 > 0.72 时警告。",
    },
    {
        "id": "alignment-near-miss",
        "check": "near_miss_alignment",
        "category": "layout",
        "en": "Left edges within 2–8pt but not equal.",
        "zh": "左边距相差 2–8pt 却未对齐。",
    },
]


def list_rules(lang: str = "en") -> list[dict[str, str]]:
    out = []
    for r in RULE_DOCS:
        out.append(
            {
                "id": r["id"],
                "check": r["check"],
                "category": r["category"],
                "description": r["zh"] if lang == "zh" else r["en"],
            }
        )
    return out
