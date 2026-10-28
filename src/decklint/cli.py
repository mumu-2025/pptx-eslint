"""decklint click CLI — bilingual help via --lang."""
from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from .engine import lint_pptx, should_fail
from .fix import NOT_AUTO_FIXED_EN, NOT_AUTO_FIXED_ZH
from .i18n import t
from .report import format_results, print_score, print_text
from .rules import list_rules

console = Console(stderr=True)


def _collect_pptx(paths: tuple[Path, ...]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        if p.is_dir():
            files.extend(sorted(p.rglob("*.pptx")))
        elif p.suffix.lower() == ".pptx":
            files.append(p)
    # skip linted outputs
    return [f for f in files if not f.name.endswith(".linted.pptx")]


@click.group()
@click.version_option(version=__version__, prog_name="decklint")
def main() -> None:
    """decklint — ESLint for PowerPoint / PowerPoint 的质量门禁.

    Not a generator: PPTX → score + violations + safe fixes.
    不是生成器：PPTX → 评分 + 违规 + 安全修复。
    """


@main.command("check")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--preset",
    type=click.Choice(["stage", "reading", "keynote", "a11y"]),
    default="stage",
    show_default=True,
    help="Rule preset / 规则预设",
)
@click.option(
    "--lang",
    type=click.Choice(["en", "zh"]),
    default="en",
    show_default=True,
    help="CLI language / 界面语言",
)
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["text", "json", "sarif", "html"]),
    default="text",
    show_default=True,
    help="Output format / 输出格式",
)
@click.option(
    "--out",
    type=click.Path(path_type=Path),
    default=None,
    help="Write report to file (html/json/sarif) / 写入报告文件",
)
@click.option(
    "--fail-on",
    type=click.Choice(["error", "warning", "info"]),
    default="error",
    show_default=True,
    help="Exit 1 threshold / 失败阈值",
)
@click.option(
    "--fix",
    "do_fix",
    is_flag=True,
    help="Apply safe auto-fixes (strip banned animations) → *.linted.pptx",
)
@click.option(
    "--rules",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Custom rules YAML / 自定义规则 YAML",
)
def check(
    paths: tuple[Path, ...],
    preset: str,
    lang: str,
    fmt: str,
    out: Path | None,
    fail_on: str,
    do_fix: bool,
    rules: Path | None,
) -> None:
    """Lint one or more .pptx files or directories.

    检查一个或多个 .pptx 文件或目录。
    """
    if not paths:
        raise click.UsageError(
            "Pass at least one .pptx path / 请至少传入一个 .pptx 路径"
        )
    files = _collect_pptx(paths)
    if not files:
        raise click.UsageError("No .pptx files found / 未找到 .pptx 文件")

    results = [
        lint_pptx(f, preset=preset, rules_path=rules, do_fix=do_fix) for f in files
    ]

    if fmt == "text":
        print_text(results, lang=lang, console=console)
        if do_fix:
            notes = NOT_AUTO_FIXED_ZH if lang == "zh" else NOT_AUTO_FIXED_EN
            console.print(
                ("[dim]Not auto-fixed:[/dim]" if lang == "en" else "[dim]不会自动修复：[/dim]")
            )
            for n in notes:
                console.print(f"  [dim]- {n}[/dim]")
    else:
        text = format_results(results, fmt=fmt, lang=lang, out=out)
        if out is None:
            click.echo(text)
        elif fmt == "text":
            pass
        else:
            console.print(f"Wrote {out}")

    failing = any(should_fail(r.violations, fail_on) for r in results)
    if failing:
        n = sum(
            1
            for r in results
            for v in r.violations
            if should_fail([v], fail_on)
        )
        console.print(t("fail_on", lang, n=n, level=fail_on), style="red")
        sys.exit(1)
    sys.exit(0)


@main.command("rules")
@click.option(
    "--lang",
    type=click.Choice(["en", "zh"]),
    default="en",
    show_default=True,
)
def rules_cmd(lang: str) -> None:
    """List registered rules / 列出已注册规则."""
    console.print(t("rules_header", lang))
    table = Table(show_header=True, header_style="bold")
    table.add_column("id")
    table.add_column("check")
    table.add_column(t("category", lang))
    table.add_column(t("message", lang))
    for r in list_rules(lang):
        table.add_row(r["id"], r["check"], r["category"], r["description"])
    console.print(table)


@main.command("score")
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--preset",
    type=click.Choice(["stage", "reading", "keynote", "a11y"]),
    default="stage",
)
@click.option("--lang", type=click.Choice(["en", "zh"]), default="en")
@click.option("--rules", type=click.Path(exists=True, path_type=Path), default=None)
def score_cmd(path: Path, preset: str, lang: str, rules: Path | None) -> None:
    """Print score breakdown by category / 按分类打印得分."""
    files = _collect_pptx((path,))
    if not files:
        raise click.UsageError("No .pptx files found / 未找到 .pptx 文件")
    for f in files:
        result = lint_pptx(f, preset=preset, rules_path=rules)
        print_score(result, lang=lang, console=console)


if __name__ == "__main__":
    main()
