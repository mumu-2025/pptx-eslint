# pptx-eslint

**ESLint for PowerPoint.** Score any `.pptx` against public design rules (Duarte · Presentation Zen · Microsoft · 优设), get machine-readable violations, and optionally auto-fix what is safe.

> Generators are everywhere. **Verifiers are almost empty.** This repo fills that gap.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CLI](https://img.shields.io/badge/cli-decklint-black)](#cli)

## Why this exists

GitHub already has many **AI PPT generators** (70k+ star tools that *create* decks). Almost nobody ships a **quality gate** for native `.pptx` the way ESLint does for JS.

If you (or your agent) generate slides, you still ship:

- wall-of-bullets “slideuments”
- 12pt text nobody in the back can read
- Excel-default chart junk
- rainbow colors with no meaning
- decorative bounce animations

`pptx-eslint` turns classic **public** tutorial principles into **checks + scores** you can run in CI, locally, or as an agent skill *after* generation.

## Not another generator

| Crowded | This repo |
|---|---|
| Prompt → PPTX | PPTX → **score + fixes** |
| Templates / themes | **Rules as code** |
| “Make it pretty” vibes | Measurable gates (font pt, contrast, SNR, chart junk…) |
| Replace Duarte/Zen books | Cite public pages; encode heuristics only |

## Quick start

```bash
pip install -e .
python scripts/make_fixtures.py   # optional sample decks
decklint check path/to/deck.pptx --preset stage
decklint check deck.pptx --preset reading --format json
decklint check deck.pptx --fix   # safe auto-fixes only
```

Exit code `1` if any `error`-severity rule fails (CI-friendly).

## Presets

| Preset | Use when | Stricter on |
|---|---|---|
| `stage` | Live talk | text density, font size |
| `reading` | Email / async review | allows denser text |
| `keynote` | Launch / keynote aesthetic | 1 accent color, very sparse text |

Rules live in [`rules/duarte-zen-microsoft.yaml`](rules/duarte-zen-microsoft.yaml).

## What we check (v0)

From public tutorials (see Sources):

1. **One idea / slide** — title-box heuristic  
2. **Text density** — chars per slide (anti-slideument)  
3. **Min font size** — back-of-room / Microsoft ≥18pt floor  
4. **Color purpose** — few non-gray accents (Duarte)  
5. **Contrast** — text vs fill WCAG-ish ratio  
6. **Chart junk** — 3D charts, heavy grids, no callouts  
7. **Animation policy** — ban decorative effects; cap transition variety  
8. **Bullet walls** — too many / too long bullets  
9. **Title as claim** — flag “Overview / 概况” style labels  
10. **Occupancy / alignment / image layout** — CRAP-ish heuristics  

## Agent skill

Drop [`skills/decklint`](skills/decklint) into your agent skills folder:

> After any `.pptx` is written, run `decklint check --preset <stage|reading|keynote>` and fix errors before delivering.

This matches the production pattern: **generators propose, verifiers decide done**.

## GitHub Action

```yaml
- uses: actions/setup-python@v5
  with: { python-version: '3.11' }
- run: pip install .
- run: decklint check **/*.pptx --preset reading
```

See [`.github/workflows/decklint.yml`](.github/workflows/decklint.yml).

## Roadmap

- [x] Rule YAML + CLI skeleton + fixtures  
- [ ] Full python-pptx static checks (v0.1)  
- [ ] `--fix` for strip-banned-animations, bump tiny fonts where safe  
- [ ] HTML/PNG contact-sheet report  
- [ ] Shared config packages (`@decklint/keynote`, `@decklint/board-reading`)  
- [ ] Corpus of anonymized before/after decks for regression  

## Sources (public pages we studied)

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
