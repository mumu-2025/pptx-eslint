"""Pluggable rule checkers. Each returns list[Violation]."""
from __future__ import annotations

from typing import Any, Callable

from pptx.slide import Slide

from ..models import Violation
from . import (
    accent_colors,
    alignment,
    animation_policy,
    auto_advance,
    box_overlap,
    bullet_depth,
    canvas,
    chart_junk,
    deck_properties,
    empty_slide,
    font_embed,
    font_families,
    image_alt,
    max_shapes,
    max_text,
    min_font,
    occupancy,
    safe_margins,
    speaker_notes,
    text_contrast,
    title_as_claim,
    title_length,
    unique_titles,
    vague_links,
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
    # v0.3
    "unique_titles": unique_titles.check,
    "safe_margins": safe_margins.check,
    "bullet_depth": bullet_depth.check,
    "speaker_notes": speaker_notes.check_speaker_notes,
    "notes_for_charts": speaker_notes.check_notes_for_charts,
    "vague_links": vague_links.check,
    "deck_properties": deck_properties.check,
    "auto_advance": auto_advance.check,
    "empty_slide": empty_slide.check,
    "max_shapes": max_shapes.check,
    "font_embed": font_embed.check,
    "title_length": title_length.check,
}

# Deck-level checkers (run once with presentation + path context)
DECK_CHECKERS: dict[str, Callable[..., list[Violation]]] = {
    "canvas_ratio": canvas.check_deck,
    "max_accent_colors": accent_colors.check_deck,
    "font_families": font_families.check_deck,
    "animation_policy": animation_policy.check_deck,
    # v0.3
    "unique_titles": unique_titles.check_deck,
    "deck_properties": deck_properties.check_deck,
    "auto_advance": auto_advance.check_deck,
    "font_embed": font_embed.check_deck,
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
    # v0.3
    {
        "id": "unique-titles",
        "check": "unique_titles",
        "category": "a11y",
        "en": "Slide titles must be unique (and preferably present).",
        "zh": "幻灯片标题须唯一（并尽量存在）。",
    },
    {
        "id": "safe-margins",
        "check": "safe_margins",
        "category": "layout",
        "en": "Keep content inside ~5% outer safe margins.",
        "zh": "内容应留在约 5% 外边距安全区内。",
    },
    {
        "id": "bullet-depth",
        "check": "bullet_depth",
        "category": "typography",
        "en": "Limit nested bullet depth.",
        "zh": "限制项目符号嵌套深度。",
    },
    {
        "id": "speaker-notes",
        "check": "speaker_notes",
        "category": "design",
        "en": "Content slides should carry speaker notes (async).",
        "zh": "内容页应有演讲者备注（异步阅读）。",
    },
    {
        "id": "notes-for-charts",
        "check": "notes_for_charts",
        "category": "chart",
        "en": "Chart slides need explanatory notes.",
        "zh": "含图表页需要说明性备注。",
    },
    {
        "id": "vague-links",
        "check": "vague_links",
        "category": "a11y",
        "en": "Ban vague hyperlink labels (click here / 了解更多).",
        "zh": "禁止含糊超链接文案（click here / 了解更多）。",
    },
    {
        "id": "deck-properties",
        "check": "deck_properties",
        "category": "a11y",
        "en": "Require core document Title (and optionally language).",
        "zh": "要求核心属性 Title（可选语言）。",
    },
    {
        "id": "auto-advance",
        "check": "auto_advance",
        "category": "a11y",
        "en": "Flag timed auto-advance transitions.",
        "zh": "标记定时自动进片。",
    },
    {
        "id": "empty-slide",
        "check": "empty_slide",
        "category": "design",
        "en": "Flag slides with no text / picture / chart.",
        "zh": "标记无文本/图片/图表的空白页。",
    },
    {
        "id": "max-shapes",
        "check": "max_shapes",
        "category": "layout",
        "en": "Too many shapes → visual clutter.",
        "zh": "形状过多 → 视觉拥挤。",
    },
    {
        "id": "font-embed",
        "check": "font_embed",
        "category": "typography",
        "en": "Prefer embedded fonts for brand QA.",
        "zh": "品牌质检建议嵌入字体。",
    },
    {
        "id": "title-length",
        "check": "title_length",
        "category": "design",
        "en": "Titles should be scannable (not stubs or paragraphs).",
        "zh": "标题应可扫读（非占位也非长段落）。",
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
