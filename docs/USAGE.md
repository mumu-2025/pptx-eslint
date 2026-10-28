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
decklint --version
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

---

## 5. Command reference

### `decklint check`

```bash
decklint check PATH... [--preset stage|reading|keynote|a11y]
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
decklint check deck.pptx --fix
decklint score deck.pptx --preset keynote --lang zh
decklint rules --lang zh
```

**Autofix does:** strip banned OOXML animations/transitions.  
**Autofix does not:** change fonts, colors, titles, layout, charts, or alt text.

---

## 6. Workflows

**Human:** export `.pptx` → `decklint check` → fix → re-run until exit 0.

**Agent / CI:** generate → `decklint check --fail-on error` → non-zero means **not done**.

See [`.github/workflows/decklint.yml`](../.github/workflows/decklint.yml) and [`skills/decklint/SKILL.md`](../skills/decklint/SKILL.md).

---

## 7. Reading results

| Field | Meaning |
|---|---|
| `score` | 0–100 |
| `Sev` | `error` / `warning` / `info` |
| `Rule` | Rule id (`decklint rules`) |
| `Slide` | 1-based index |

Rule encyclopedia: [`rules.md`](rules.md)

---

## 8. FAQ

**`command not found`** — activate the venv and `pip install -e .`.

**Bad contrast not reported** — only solid RGB pairs are measured; theme/gradient/picture fills are skipped to avoid false positives.

**`.ppt` old format** — not supported; save as `.pptx`.

**vs generators (ppt-master, Gamma…)** — they create; `decklint` verifies. Chain them.

---

## 9. Dev / tests

```bash
pip install -e ".[dev]"
python scripts/make_fixtures.py
pytest -q
```

---

## 10. Help

```bash
decklint --help
decklint check --help
```

Repo: https://github.com/mumu-2025/pptx-eslint
