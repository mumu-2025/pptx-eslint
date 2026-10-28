"""CLI / report string catalogs (en | zh)."""
from __future__ import annotations

MESSAGES: dict[str, dict[str, str]] = {
    "clean": {
        "en": "✓ clean",
        "zh": "✓ 通过",
    },
    "score_line": {
        "en": "{file}  score={score}/100  preset={preset}",
        "zh": "{file}  得分={score}/100  预设={preset}",
    },
    "sev": {"en": "Sev", "zh": "级别"},
    "rule": {"en": "Rule", "zh": "规则"},
    "slide": {"en": "Slide", "zh": "页"},
    "category": {"en": "Category", "zh": "分类"},
    "message": {"en": "Message", "zh": "说明"},
    "fix_hint": {"en": "Fix", "zh": "修复建议"},
    "category_breakdown": {
        "en": "Score by category",
        "zh": "分类得分",
    },
    "rules_header": {
        "en": "Available rules",
        "zh": "可用规则",
    },
    "fixed_written": {
        "en": "Wrote fixed deck: {path}",
        "zh": "已写入修复稿：{path}",
    },
    "fail_on": {
        "en": "Failing: {n} violation(s) at or above '{level}'",
        "zh": "失败：{n} 条不低于「{level}」的违规",
    },
    "cli_main": {
        "en": "Lint native .pptx decks against public design rules (ESLint for PowerPoint).",
        "zh": "对照公开设计规则检查原生 .pptx（PowerPoint 的 ESLint）。",
    },
    "cli_check": {
        "en": "Lint one or more .pptx files or directories.",
        "zh": "检查一个或多个 .pptx 文件或目录。",
    },
    "cli_rules": {
        "en": "List registered rules.",
        "zh": "列出已注册规则。",
    },
    "cli_score": {
        "en": "Print category score breakdown for a deck.",
        "zh": "打印幻灯片分类得分明细。",
    },
}


def t(key: str, lang: str = "en", **kwargs: object) -> str:
    catalog = MESSAGES.get(key) or {}
    template = catalog.get(lang) or catalog.get("en") or key
    return template.format(**kwargs) if kwargs else template
