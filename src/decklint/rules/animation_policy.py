"""animation-policy — OOXML timing/transition checks."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..models import Violation
from ..ooxml import parse_slide_animations


def check(slide, idx: int, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    return []


def check_deck(prs, path, rule: dict[str, Any], ctx: dict[str, Any]) -> list[Violation]:
    path = Path(path)
    ban = [b.lower() for b in (rule.get("ban_effects") or ["bounce", "spiral", "growTurn", "swish", "whip"])]
    max_trans = int(rule.get("max_distinct_transitions", 3))
    try:
        slides_meta = parse_slide_animations(path)
    except Exception:
        return []

    out: list[Violation] = []
    all_transitions: set[str] = set()
    for meta in slides_meta:
        all_transitions.update(meta.get("transitions") or [])
        effects = [e.lower() for e in (meta.get("effects") or [])]
        hit = sorted({b for b in ban if any(b in e for e in effects)})
        if hit:
            out.append(
                Violation(
                    rule_id="animation-policy",
                    severity=rule.get("_severity", "warning"),
                    slide=meta.get("slide"),
                    message_en=f"banned decorative animation hint(s): {', '.join(hit)}",
                    message_zh=f"禁用装饰性动画线索：{', '.join(hit)}",
                    fix_hint_en="Remove bounce/spiral/etc.; use simple appear/fade for pacing only. Or: decklint check --fix",
                    fix_hint_zh="去掉 bounce/spiral 等；仅用简单出现/淡入控制节奏。或：decklint check --fix",
                    category="animation",
                )
            )
    # filter empty / none-like
    meaningful = {t for t in all_transitions if t and t.lower() not in ("transition",)}
    if len(meaningful) > max_trans:
        out.append(
            Violation(
                rule_id="animation-policy",
                severity=rule.get("_severity", "warning"),
                slide=None,
                message_en=f"{len(meaningful)} distinct transition types (max {max_trans})",
                message_zh=f"{len(meaningful)} 种切换效果（上限 {max_trans}）",
                fix_hint_en="Pick one quiet transition family and reuse it.",
                fix_hint_zh="选定一种安静的切换并复用。",
                category="animation",
            )
        )
    return out
