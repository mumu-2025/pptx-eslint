"""decklint — ESLint for PowerPoint."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from .engine import lint_pptx

console = Console(stderr=True)


@click.group()
@click.version_option(package_name="decklint")
def main() -> None:
    """Lint native .pptx decks against public design rules."""


@main.command("check")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--preset",
    type=click.Choice(["stage", "reading", "keynote", "core"]),
    default="stage",
    show_default=True,
)
@click.option("--format", "fmt", type=click.Choice(["text", "json"]), default="text")
@click.option("--rules", type=click.Path(exists=True, path_type=Path), default=None)
@click.option("--fix", "do_fix", is_flag=True, help="Apply safe auto-fixes (v0: animations strip stub).")
def check(paths: tuple[Path, ...], preset: str, fmt: str, rules: Path | None, do_fix: bool) -> None:
    if not paths:
        raise click.UsageError("Pass at least one .pptx path")
    files = []
    for p in paths:
        if p.is_dir():
            files.extend(sorted(p.rglob("*.pptx")))
        elif p.suffix.lower() == ".pptx":
            files.append(p)
    if not files:
        raise click.UsageError("No .pptx files found")

    all_results = []
    errors = 0
    for f in files:
        result = lint_pptx(f, preset=preset, rules_path=rules, do_fix=do_fix)
        all_results.append(result)
        errors += sum(1 for v in result["violations"] if v["severity"] == "error")

    if fmt == "json":
        click.echo(json.dumps(all_results, ensure_ascii=False, indent=2))
    else:
        for result in all_results:
            _print_text(result)

    sys.exit(1 if errors else 0)


def _print_text(result: dict) -> None:
    console.print(f"\n[bold]{result['file']}[/bold]  score={result['score']}/100  preset={result['preset']}")
    if not result["violations"]:
        console.print("[green]✓ clean[/green]")
        return
    table = Table(show_header=True, header_style="bold")
    table.add_column("Sev")
    table.add_column("Rule")
    table.add_column("Slide")
    table.add_column("Message")
    for v in result["violations"]:
        sev = {"error": "red", "warning": "yellow", "info": "cyan"}.get(v["severity"], "white")
        table.add_row(f"[{sev}]{v['severity']}[/{sev}]", v["rule"], str(v.get("slide", "-")), v["message"])
    console.print(table)


if __name__ == "__main__":
    main()
