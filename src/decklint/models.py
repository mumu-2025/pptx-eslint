"""Shared data models for decklint violations."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


SEVERITIES = ("error", "warning", "info")
CATEGORIES = (
    "design",
    "typography",
    "color",
    "layout",
    "chart",
    "animation",
    "a11y",
)


@dataclass
class Violation:
    rule_id: str
    severity: str
    slide: int | None
    message_en: str
    message_zh: str
    fix_hint_en: str = ""
    fix_hint_zh: str = ""
    category: str = "design"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def message(self, lang: str = "en") -> str:
        return self.message_zh if lang == "zh" else self.message_en

    def fix_hint(self, lang: str = "en") -> str:
        return self.fix_hint_zh if lang == "zh" else self.fix_hint_en


@dataclass
class LintResult:
    file: str
    preset: str
    score: int
    violations: list[Violation] = field(default_factory=list)
    fixed_path: str | None = None
    category_scores: dict[str, int] = field(default_factory=dict)

    def to_dict(self, lang: str = "en") -> dict[str, Any]:
        return {
            "file": self.file,
            "preset": self.preset,
            "score": self.score,
            "category_scores": self.category_scores,
            "fixed_path": self.fixed_path,
            "violations": [
                {
                    **v.to_dict(),
                    "message": v.message(lang),
                    "fix_hint": v.fix_hint(lang),
                }
                for v in self.violations
            ],
        }
