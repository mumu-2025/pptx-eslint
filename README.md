# pptx-eslint / decklint

**ESLint for PowerPoint** · **PowerPoint 的 ESLint**

Score any `.pptx` against public design rules (Duarte · Presentation Zen · Microsoft · 优设), get machine-readable violations (JSON / SARIF / HTML), and optionally auto-fix what is safe.

> Generators are everywhere. **Verifiers are almost empty.** This repo fills that gap.  
> 生成器到处都是。**校验器几乎空白。** 本仓库补上这块缺口。

中文完整说明 → [`README.zh-CN.md`](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CLI](https://img.shields.io/badge/cli-decklint-black)](#cli)
[![version](https://img.shields.io/badge/version-0.2.1-green)](pyproject.toml)

## Why this exists

GitHub already has many **AI PPT generators**. Almost nobody ships a **quality gate** for native `.pptx` the way ESLint does for JS.

If you (or your agent) generate slides, you still ship slideuments, tiny fonts, chart junk, rainbow accents, and bounce animations.

`decklint` turns classic **public** tutorial principles into **checks + scores** for CI, local use, or an agent skill *after* generation.

## Not another generator

| Crowded | This repo |
|---|---|
| Prompt → PPTX | PPTX → **score + fixes** |
| Templates / themes | **Rules as code** |
| “Make it pretty” vibes | Measurable gates (font pt, WCAG contrast, occupancy…) |
| Replace Duarte/Zen books | Cite public pages; encode heuristics only |


## How to use (full guide)

👉 **Step-by-step install, presets, CI / agents, FAQ:** [`docs/USAGE.md`](docs/USAGE.md) · 中文 [`docs/USAGE.zh-CN.md`](docs/USAGE.zh-CN.md)

Shortest path:

```bash
git clone https://github.com/mumu-2025/pptx-eslint.git
cd pptx-eslint
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python scripts/make_fixtures.py
decklint check fixtures/bad/slideument.pptx --preset stage
decklint check your.pptx --preset reading --lang zh --format html --out report.html
```

| Goal | Command |
|---|---|
| Live talk deck | `decklint check x.pptx --preset stage` |
| Email / async reading | `decklint check x.pptx --preset reading` |
| Keynote-style | `decklint check x.pptx --preset keynote` |
| Accessibility gate | `decklint check x.pptx --preset a11y` |
| List rules | `decklint rules --lang zh` |
| Category scores | `decklint score x.pptx` |
| HTML report | `... --format html --out report.html` |
| Safe animation strip | `... --fix` → `*.linted.pptx` |

## Quick start

```bash
pip install -e ".[dev]"
python scripts/make_fixtures.py
decklint check path/to/deck.pptx --preset stage
decklint check deck.pptx --preset reading --lang zh --format json
decklint check deck.pptx --format sarif --out report.sarif
decklint check deck.pptx --format html --out report.html
decklint check deck.pptx --fix          # safe auto-fixes only → *.linted.pptx
decklint rules --lang zh
decklint score deck.pptx --preset keynote
```

Exit code `1` when violations meet `--fail-on` (default: `error`).

## Presets

| Preset | Use when | Stricter on |
|---|---|---|
| `stage` | Live talk | text density, font size |
| `reading` | Email / async review | denser text allowed |
| `keynote` | Launch aesthetic | 1 accent, very sparse text |
| `a11y` | Accessibility gate | WCAG contrast + required image alt |

Rules: [`rules/duarte-zen-microsoft.yaml`](rules/duarte-zen-microsoft.yaml) · [`rules/accessibility.yaml`](rules/accessibility.yaml)

## What we check (v0.2)

| Category | Rules |
|---|---|
| typography | `max-text`, `no-slideument`, `min-font`, `font-families` |
| color / a11y | `accent-colors`, `text-contrast` (WCAG), `image-alt`, `a11y-title` |
| layout | `occupancy`, `alignment-near-miss`, `box-overlap`, `image-bleed` |
| design | `one-idea`, `title-as-claim`, `canvas` (16:9) |
| chart | `chart-junk` (3D + callout reminder) |
| animation | `animation-policy` (OOXML timing / transitions) |

See [`docs/rules.md`](docs/rules.md) / [`docs/rules.zh-CN.md`](docs/rules.zh-CN.md).

## `--fix` (safe only)

**Does:** strip banned animation / transition nodes from OOXML when identifiable → writes `*.linted.pptx`.

**Does not:** rewrite titles, fonts, colors, layout, charts, alt text, or aspect ratio. See `decklint.fix` module docstring.

## Agent skill

[`skills/decklint`](skills/decklint) — after any `.pptx` is written, run `decklint check` and fix errors before delivering.

## GitHub Action

See [`.github/workflows/decklint.yml`](.github/workflows/decklint.yml) — installs, fixtures, pytest, bad/good gates, SARIF artifact.

## Sources (public pages)

- Duarte — [4 presentation design principles](https://www.duarte.com/blog/4-presentation-design-principles-to-live-by/)
- Garr Reynolds — [Design tips](https://www.garrreynolds.com/design-tips)
- Microsoft Support — [Effective presentation tips](https://support.microsoft.com/en-us/powerpoint/tips-for-creating-and-delivering-an-effective-presentation)
- 优设 / 少数派 — public workplace PPT craft articles

We do **not** copy book chapters. Rules are measurable heuristics inspired by those public pages.

## License

MIT. Tutorial brands and books remain their owners’.

---

### Star if you want “CI for slides”

If AI can generate 50 decks a day, someone has to **fail the bad ones**. That’s this repo.
