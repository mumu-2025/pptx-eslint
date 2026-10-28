"""Safe auto-fixes for decklint.

What IS auto-fixed (--fix):
- Strip banned animation / transition nodes from OOXML when identifiable
  (bounce, spiral, growTurn, swish, whip, …). Writes *.linted.pptx.

What is NOT auto-fixed (by design):
- Text content / titles / claims
- Font sizes or families
- Colors / contrast (needs design judgment)
- Layout, overlap, occupancy, alignment
- Chart type conversion
- Image alt text content (we only detect missing)
- Slide canvas / aspect ratio
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .ooxml import strip_banned_animations


def apply_safe_fixes(
    path: Path,
    params: dict[str, Any] | None = None,
    out_path: Path | None = None,
) -> Path:
    """Apply safe fixes; return path of written *.linted.pptx."""
    params = params or {}
    anim = params.get("animation_policy") or params.get("animation-policy") or {}
    ban = list(anim.get("ban_effects") or [])
    dest = out_path or path.with_name(path.stem + ".linted.pptx")
    strip_banned_animations(path, dest, ban_effects=ban or None)
    return dest


NOT_AUTO_FIXED_EN = [
    "Text content, titles, and claim wording",
    "Font sizes and typeface choices",
    "Colors and contrast adjustments",
    "Layout, overlap, occupancy, alignment",
    "Chart type conversion / chart junk cleanup",
    "Writing image alt / descr text",
    "Changing slide aspect ratio",
]

NOT_AUTO_FIXED_ZH = [
    "正文、标题与主张措辞",
    "字号与字体选择",
    "颜色与对比度调整",
    "版式、重叠、占版率、对齐",
    "图表类型转换 / 图表垃圾清理",
    "撰写图片替代文本",
    "修改幻灯片画布比例",
]
