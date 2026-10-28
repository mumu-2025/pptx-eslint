# Usage guide (English)

`decklint` **audits existing** `.pptx` files. It scores them and lists violations. It does **not** generate slides.

中文 → [`USAGE.zh-CN.md`](USAGE.zh-CN.md)

---

## 1. Requirements

- Python **3.10+**
- macOS / Linux / Windows (WSL fine)
- Microsoft PowerPoint is **not** required

---

## 2. Install

### A. Clone from GitHub (recommended)

```bash
git clone https://github.com/mumu-2025/pptx-eslint.git
cd pptx-eslint
python -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -e ".[dev]"
decklint --version                 # expect 0.3.x
```

### B. Local folder

```bash
cd /path/to/pptx-eslint
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

---

## 3. Five-minute start

```bash
python scripts/make_fixtures.py
decklint check fixtures/bad/slideument.pptx --preset stage
decklint check fixtures/good/claim-slide.pptx --preset stage   # expect exit 0
decklint check /path/to/your.pptx --preset reading --lang zh
```

Directories are scanned recursively for `*.pptx`.

---

## 4. Pick a preset

| Preset | When | Notes |
|---|---|---|
| `stage` | Live talk (default) | Sparse text, large fonts |
| `reading` | Email / async review | Allows denser text |
| `keynote` | Launch / keynote look | Fewer accents, stricter density |
| `a11y` | Accessibility gate | WCAG contrast + image alt |
| `corporate` | Brand / enterprise QA | Fonts ≤2, accents ≤2, margins, embed fonts, file Title |
| `wcag-strict` | Strict accessibility | Unique titles + alt + no auto-advance as **errors** |
| `async-doc` | Read-without-speaker handoff | Requires speaker notes on content slides |

---

## 5. Command reference

### `decklint check`

```bash
decklint check PATH... [--preset stage|reading|keynote|a11y|corporate|wcag-strict|async-doc]
                       [--lang en|zh]
                       [--format text|json|sarif|html]
                       [--out FILE]
                       [--fail-on error|warning|info]
                       [--fix]
                       [--rules RULES.yaml]
```

| Flag | Meaning | Default |
|---|---|---|
| `--preset` | Rule pack | `stage` |
| `--lang` | Message language | `en` |
| `--format` | Output shape | `text` |
| `--out` | Write report file | — |
| `--fail-on` | Exit 1 from this severity up | `error` |
| `--fix` | Safe autofix → `*.linted.pptx` | off |

Examples:

```bash
decklint check deck.pptx --lang zh --format html --out report.html
decklint check deck.pptx --format json --out report.json
decklint check deck.pptx --format sarif --out decklint.sarif
decklint check deck.pptx --preset corporate --fail-on warning
decklint check deck.pptx --preset wcag-strict --lang zh
decklint check deck.pptx --preset async-doc
decklint check deck.pptx --fix
decklint score deck.pptx --preset keynote --lang zh
decklint rules --lang zh
```

**Autofix does:** strip banned OOXML animations/transitions.  
**Autofix does not:** change fonts, colors, titles, layout, charts, alt text, notes, or margins.

---

## 6. All rules (v0.3)

| Rule id | Category | What it checks |
|---|---|---|
| `max-text` | typography | Characters per slide |
| `no-slideument` | typography | Bullet walls / long bullets |
| `min-font` | typography | Minimum explicit font size |
| `font-families` | typography | Distinct typeface count |
| `font-embed` | typography | Embedded fonts in OOXML (corporate) |
| `bullet-depth` | typography | Nested bullet depth |
| `accent-colors` | color | Non-gray accent count |
| `text-contrast` | a11y | WCAG contrast (solid RGB) |
| `image-alt` | a11y | Picture descr / alt |
| `a11y-title` | a11y | Title placeholder on titled layouts |
| `unique-titles` | a11y | Unique (and present) slide titles |
| `vague-links` | a11y | Ban "click here" / "了解更多" |
| `auto-advance` | a11y | Timed `advTm` transitions |
| `deck-properties` | a11y | Core document Title |
| `occupancy` | layout | Shape fill ratio |
| `alignment-near-miss` | layout | Near-miss left edges |
| `box-overlap` | layout | Opaque overlap |
| `image-bleed` | layout | Too many pictures |
| `safe-margins` | layout | ~5% outer safe area |
| `max-shapes` | layout | Shape clutter cap |
| `one-idea` | design | Multiple top text frames |
| `title-as-claim` | design | Vague titles |
| `title-length` | design | Title too short / too long |
| `empty-slide` | design | Blank slides |
| `speaker-notes` | design | Notes on content slides (async-doc) |
| `canvas` | design | Prefer ~16:9 |
| `chart-junk` | chart | 3D / callout reminder |
| `notes-for-charts` | chart | Chart slides need notes |
| `animation-policy` | animation | Ban decorative effects; cap transitions |

Full encyclopedia: [`rules.md`](rules.md)

---

## 7. Workflows

**Human:** export `.pptx` → `decklint check` → fix → re-run until exit 0.

**Agent / CI:** generate → `decklint check --fail-on error` → non-zero means **not done**.

### CI example (GitHub Actions)

```yaml
- run: pip install -e ".[dev]"
- run: decklint check decks/ --preset corporate --fail-on warning --format sarif --out decklint.sarif
```

See [`.github/workflows/decklint.yml`](../.github/workflows/decklint.yml) and [`skills/decklint/SKILL.md`](../skills/decklint/SKILL.md).

---

## 8. Reading results

| Field | Meaning |
|---|---|
| `score` | 0–100 |
| `Sev` | `error` / `warning` / `info` |
| `Rule` | Rule id (`decklint rules`) |
| `Slide` | 1-based index (empty = whole deck) |

---

## 9. FAQ

**`command not found`** — activate the venv and `pip install -e .`.

**Bad contrast not reported** — only solid RGB pairs are measured; theme/gradient/picture fills are skipped to avoid false positives.

**`.ppt` old format** — not supported; save as `.pptx`.

**vs generators (ppt-master, Gamma…)** — they create; `decklint` verifies. Chain them.

**Why so many info findings on a fresh deck?** — `deck-properties` / `font-embed` are soft by default; use `corporate` or `wcag-strict` when you want them enforced.

---

## 10. Dev / tests

```bash
pip install -e ".[dev]"
python scripts/make_fixtures.py
pytest -q
```

---

## 11. Help

```bash
decklint --help
decklint check --help
```

Repo: https://github.com/mumu-2025/pptx-eslint
