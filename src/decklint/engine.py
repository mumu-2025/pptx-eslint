"""Orchestrate linting: load presets, run pluggable rules, score."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pptx import Presentation

from .fix import apply_safe_fixes
from .models import LintResult, Violation
from .rules import CHECKERS, DECK_CHECKERS

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RULES = ROOT / "rules" / "duarte-zen-microsoft.yaml"
A11Y_RULES = ROOT / "rules" / "accessibility.yaml"
CORPORATE_RULES = ROOT / "rules" / "corporate.yaml"
WCAG_STRICT_RULES = ROOT / "rules" / "wcag-strict.yaml"
ASYNC_DOC_RULES = ROOT / "rules" / "async-doc.yaml"

PRESETS = (
    "stage",
    "reading",
    "keynote",
    "a11y",
    "corporate",
    "wcag-strict",
    "async-doc",
)

# Extra YAML packs merged for specific presets (order matters).
PRESET_EXTRA_FILES: dict[str, list[Path]] = {
    "a11y": [A11Y_RULES],
    "wcag-strict": [A11Y_RULES, WCAG_STRICT_RULES],
    "corporate": [CORPORATE_RULES],
    "async-doc": [ASYNC_DOC_RULES],
}

# Map preset override keys → check param keys
OVERRIDE_MAP = {
    "max_chars_per_slide": ("max_chars_per_slide", "max"),
    "min_font_pt": ("min_font_pt", "min"),
    "max_accent_colors": ("max_accent_colors", "max"),
    "max_fill_ratio": ("occupancy", "max_fill_ratio"),
    "min_ratio": ("text_bg_contrast", "min_ratio"),
    "max_font_families": ("font_families", "max"),
}


def load_rules(path: Path | None, preset: str) -> dict[str, Any]:
    primary = path or DEFAULT_RULES
    data = yaml.safe_load(primary.read_text(encoding="utf-8")) or {}

    for extra_path in PRESET_EXTRA_FILES.get(preset, []):
        if extra_path.exists():
            extra = yaml.safe_load(extra_path.read_text(encoding="utf-8")) or {}
            data = _merge_rule_docs(data, extra)

    params: dict[str, Any] = {}
    for rule in data.get("rules", []):
        check = rule["check"]
        entry = dict(rule.get("params") or {})
        entry["_severity"] = rule.get("severity", "warning")
        entry["_id"] = rule.get("id", check)
        entry["_description"] = rule.get("description", "")
        entry["_description_zh"] = rule.get("description_zh", "")
        entry["_category"] = rule.get("category", "design")
        params[check] = entry

    presets = data.get("presets") or {}
    # resolve extends chain
    overrides = _resolve_preset_overrides(presets, preset)
    for key, value in overrides.items():
        if key in OVERRIDE_MAP:
            check, param = OVERRIDE_MAP[key]
            params.setdefault(
                check,
                {
                    "_severity": "warning",
                    "_id": check,
                    "_description": key,
                    "_category": "design",
                },
            )
            params[check][param] = value
        elif key in params:
            # direct check-level override dict
            if isinstance(value, dict):
                params[key].update(value)
            else:
                params[key]["value"] = value
        else:
            # stash soft knobs
            params.setdefault(key, {"_severity": "info", "_id": key, "_category": "design"})
            if isinstance(value, dict):
                params[key].update(value)
            else:
                params[key]["value"] = value

    return {"raw": data, "params": params, "preset": preset}


def _resolve_preset_overrides(presets: dict, name: str) -> dict[str, Any]:
    if name not in presets:
        return {}
    node = presets[name] or {}
    acc: dict[str, Any] = {}
    for parent in node.get("extends") or []:
        acc.update(_resolve_preset_overrides(presets, parent))
    acc.update(node.get("overrides") or {})
    return acc


def _merge_rule_docs(base: dict, extra: dict) -> dict:
    out = dict(base)
    out_rules = list(base.get("rules") or [])
    by_id = {r.get("id"): i for i, r in enumerate(out_rules)}
    for rule in extra.get("rules") or []:
        rid = rule.get("id")
        if rid in by_id:
            # merge params / bump severity
            existing = dict(out_rules[by_id[rid]])
            existing["severity"] = rule.get("severity", existing.get("severity"))
            merged_params = dict(existing.get("params") or {})
            merged_params.update(rule.get("params") or {})
            existing["params"] = merged_params
            if rule.get("description"):
                existing["description"] = rule["description"]
            if rule.get("description_zh"):
                existing["description_zh"] = rule["description_zh"]
            out_rules[by_id[rid]] = existing
        else:
            out_rules.append(rule)
            by_id[rid] = len(out_rules) - 1
    out["rules"] = out_rules
    # merge presets
    presets = dict(base.get("presets") or {})
    presets.update(extra.get("presets") or {})
    out["presets"] = presets
    return out


def lint_pptx(
    path: Path,
    preset: str = "stage",
    rules_path: Path | None = None,
    do_fix: bool = False,
) -> LintResult:
    path = Path(path)
    cfg = load_rules(rules_path, preset)
    params = cfg["params"]
    prs = Presentation(str(path))
    ctx: dict[str, Any] = {"prs": prs, "path": path, "preset": preset}
    violations: list[Violation] = []

    # Per-slide checkers
    for i, slide in enumerate(prs.slides, start=1):
        for check_name, fn in CHECKERS.items():
            if check_name not in params:
                continue
            if check_name in DECK_CHECKERS:
                # skip per-slide no-op stubs; deck-level handles
                continue
            try:
                violations.extend(fn(slide, i, params[check_name], ctx))
            except Exception as exc:  # noqa: BLE001 — keep linting robust
                violations.append(
                    Violation(
                        rule_id=params[check_name].get("_id", check_name),
                        severity="info",
                        slide=i,
                        message_en=f"checker {check_name} error: {exc}",
                        message_zh=f"检查器 {check_name} 异常：{exc}",
                        category=params[check_name].get("_category", "design"),
                    )
                )

    # Deck-level checkers
    for check_name, fn in DECK_CHECKERS.items():
        if check_name not in params:
            continue
        try:
            violations.extend(fn(prs, path, params[check_name], ctx))
        except Exception as exc:  # noqa: BLE001
            violations.append(
                Violation(
                    rule_id=params[check_name].get("_id", check_name),
                    severity="info",
                    slide=None,
                    message_en=f"deck checker {check_name} error: {exc}",
                    message_zh=f"整稿检查器 {check_name} 异常：{exc}",
                    category=params[check_name].get("_category", "design"),
                )
            )

    fixed_path = None
    if do_fix:
        fixed_path = str(apply_safe_fixes(path, params))

    score, category_scores = compute_scores(violations)
    return LintResult(
        file=str(path),
        preset=preset,
        score=score,
        violations=violations,
        fixed_path=fixed_path,
        category_scores=category_scores,
    )


def compute_scores(violations: list[Violation]) -> tuple[int, dict[str, int]]:
    from .models import CATEGORIES

    score = 100
    cat = {c: 100 for c in CATEGORIES}
    weights = {"error": 12, "warning": 5, "info": 1}
    for v in violations:
        w = weights.get(v.severity, 3)
        score -= w
        if v.category in cat:
            cat[v.category] -= w
    score = max(0, score)
    cat = {k: max(0, v) for k, v in cat.items()}
    return score, cat


def severity_rank(sev: str) -> int:
    return {"info": 1, "warning": 2, "error": 3}.get(sev, 0)


def should_fail(violations: list[Violation], fail_on: str) -> bool:
    threshold = severity_rank(fail_on)
    return any(severity_rank(v.severity) >= threshold for v in violations)
