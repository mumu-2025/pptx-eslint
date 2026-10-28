"""Formatters: text (rich), json, sarif, html."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

from .i18n import t
from .models import LintResult, Violation


def format_results(
    results: list[LintResult],
    fmt: str,
    lang: str = "en",
    out: Path | None = None,
) -> str:
    if fmt == "json":
        text = json.dumps([r.to_dict(lang) for r in results], ensure_ascii=False, indent=2)
    elif fmt == "sarif":
        text = json.dumps(to_sarif(results), ensure_ascii=False, indent=2)
    elif fmt == "html":
        text = to_html(results, lang)
    else:
        text = ""
        # text uses rich to stderr/stdout via print_text
        return text

    if out:
        out.write_text(text, encoding="utf-8")
    return text


def print_text(results: list[LintResult], lang: str = "en", console: Console | None = None) -> None:
    console = console or Console()
    for result in results:
        console.print(
            t(
                "score_line",
                lang,
                file=result.file,
                score=result.score,
                preset=result.preset,
            )
        )
        if not result.violations:
            console.print(f"[green]{t('clean', lang)}[/green]")
            continue
        table = Table(show_header=True, header_style="bold")
        table.add_column(t("sev", lang))
        table.add_column(t("rule", lang))
        table.add_column(t("category", lang))
        table.add_column(t("slide", lang))
        table.add_column(t("message", lang))
        for v in result.violations:
            sev_style = {"error": "red", "warning": "yellow", "info": "cyan"}.get(v.severity, "white")
            table.add_row(
                f"[{sev_style}]{v.severity}[/{sev_style}]",
                v.rule_id,
                v.category,
                str(v.slide if v.slide is not None else "-"),
                v.message(lang),
            )
        console.print(table)
        if result.fixed_path:
            console.print(t("fixed_written", lang, path=result.fixed_path))


def print_score(result: LintResult, lang: str = "en", console: Console | None = None) -> None:
    console = console or Console()
    console.print(
        t(
            "score_line",
            lang,
            file=result.file,
            score=result.score,
            preset=result.preset,
        )
    )
    console.print(t("category_breakdown", lang))
    table = Table(show_header=True, header_style="bold")
    table.add_column(t("category", lang))
    table.add_column("Score")
    for cat, sc in sorted(result.category_scores.items()):
        table.add_row(cat, str(sc))
    console.print(table)


def to_sarif(results: list[LintResult]) -> dict[str, Any]:
    """GitHub Code Scanning compatible SARIF 2.1.0."""
    rules_seen: dict[str, Violation] = {}
    for r in results:
        for v in r.violations:
            rules_seen.setdefault(v.rule_id, v)

    sarif_rules = []
    for rid, sample in rules_seen.items():
        sarif_rules.append(
            {
                "id": rid,
                "name": rid,
                "shortDescription": {"text": sample.message_en},
                "fullDescription": {"text": sample.message_en},
                "defaultConfiguration": {
                    "level": _sarif_level(sample.severity),
                },
                "properties": {"tags": [sample.category]},
            }
        )

    runs_results = []
    for r in results:
        for v in r.violations:
            runs_results.append(
                {
                    "ruleId": v.rule_id,
                    "level": _sarif_level(v.severity),
                    "message": {
                        "text": v.message_en,
                        "properties": {
                            "message_zh": v.message_zh,
                            "fix_hint_en": v.fix_hint_en,
                            "fix_hint_zh": v.fix_hint_zh,
                        },
                    },
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": r.file},
                                "region": {
                                    "startLine": v.slide or 1,
                                },
                            }
                        }
                    ],
                    "properties": {"category": v.category, "slide": v.slide},
                }
            )

    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "decklint",
                        "informationUri": "https://github.com/pptx-eslint/pptx-eslint",
                        "rules": sarif_rules,
                    }
                },
                "results": runs_results,
            }
        ],
    }


def to_html(results: list[LintResult], lang: str = "en") -> str:
    rows = []
    for r in results:
        rows.append(
            f"<h2>{_esc(r.file)} — score {r.score}/100 ({r.preset})</h2>"
        )
        if not r.violations:
            rows.append(f"<p class='ok'>{_esc(t('clean', lang))}</p>")
            continue
        rows.append(
            "<table><thead><tr>"
            f"<th>{_esc(t('sev', lang))}</th>"
            f"<th>{_esc(t('rule', lang))}</th>"
            f"<th>{_esc(t('category', lang))}</th>"
            f"<th>{_esc(t('slide', lang))}</th>"
            f"<th>{_esc(t('message', lang))}</th>"
            f"<th>{_esc(t('fix_hint', lang))}</th>"
            "</tr></thead><tbody>"
        )
        for v in r.violations:
            rows.append(
                "<tr>"
                f"<td class='{v.severity}'>{_esc(v.severity)}</td>"
                f"<td>{_esc(v.rule_id)}</td>"
                f"<td>{_esc(v.category)}</td>"
                f"<td>{v.slide if v.slide is not None else '-'}</td>"
                f"<td>{_esc(v.message(lang))}</td>"
                f"<td>{_esc(v.fix_hint(lang))}</td>"
                "</tr>"
            )
        rows.append("</tbody></table>")

    body = "\n".join(rows)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"/>
<title>decklint report</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem; background: #0b0b0c; color: #eee; }}
h1,h2 {{ font-weight: 600; }}
table {{ border-collapse: collapse; width: 100%; margin-bottom: 2rem; }}
th, td {{ border: 1px solid #333; padding: 0.5rem 0.75rem; text-align: left; }}
th {{ background: #1a1a1e; }}
.error {{ color: #ff6b6b; }}
.warning {{ color: #ffd93d; }}
.info {{ color: #6bcBff; }}
.ok {{ color: #6bffb8; }}
</style>
</head>
<body>
<h1>decklint</h1>
{body}
</body>
</html>
"""


def _sarif_level(severity: str) -> str:
    return {"error": "error", "warning": "warning", "info": "note"}.get(severity, "warning")


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
