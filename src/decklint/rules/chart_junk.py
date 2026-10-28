"""chart-junk — detect charts; flag 3D-ish; info for callouts."""
from __future__ import annotations

from typing import Any

from ..models import Violation


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    out: list[Violation] = []
    ban_3d = bool(rule.get("ban_3d", True))
    for shape in slide.shapes:
        if not getattr(shape, "has_chart", False):
            continue
        try:
            chart = shape.chart
            type_name = ""
            try:
                type_name = str(chart.chart_type)
            except Exception:
                type_name = ""
            is_3d = "3D" in type_name.upper() or "THREE" in type_name.upper()
            if ban_3d and is_3d:
                out.append(
                    Violation(
                        rule_id="chart-junk",
                        severity=rule.get("_severity", "warning"),
                        slide=idx,
                        message_en=f"3D chart type detected ({type_name})",
                        message_zh=f"检测到 3D 图表类型（{type_name}）",
                        fix_hint_en="Switch to a flat 2D chart; 3D distorts comparison.",
                        fix_hint_zh="改用平面 2D 图；3D 会扭曲比较。",
                        category="chart",
                    )
                )
            if rule.get("require_data_labels_or_callouts", True):
                out.append(
                    Violation(
                        rule_id="chart-junk",
                        severity="info",
                        slide=idx,
                        message_en="chart present — ensure callouts / labels, not default Excel chrome",
                        message_zh="存在图表 — 请确认有标注/数据标签，而非 Excel 默认装饰",
                        fix_hint_en="Add a callout for the takeaway number; strip heavy gridlines.",
                        fix_hint_zh="为关键数字加标注；去掉沉重网格线。",
                        category="chart",
                    )
                )
        except Exception:
            out.append(
                Violation(
                    rule_id="chart-junk",
                    severity="info",
                    slide=idx,
                    message_en="chart present — manually review for junk",
                    message_zh="存在图表 — 请人工检查是否有图表垃圾",
                    fix_hint_en="Review chart styling against Duarte 'don't be default'.",
                    fix_hint_zh="对照 Duarte「不要默认样式」检查图表。",
                    category="chart",
                )
            )
    return out
