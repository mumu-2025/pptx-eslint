# Competitive gap (research 2026-10-28, updated for v0.2)

中文版 → [`COMPETITIVE-GAP.zh-CN.md`](COMPETITIVE-GAP.zh-CN.md)

## Crowded (do not clone)

| Area | Examples (stars order-of-magnitude) |
|---|---|
| AI → PPTX generators | ppt-master (~70k), presenton, banana-slides, PPTist |
| Agent skills that *generate* slides | guizang-ppt-skill, html-ppt-skill, dashi-ppt-skill, Kami, huashu-design |
| HTML slide frameworks | reveal.js, slidev, marp, spectacle |
| Office agent harness | OfficeCLI, Univer, genoffice |

## Nearly empty

| Area | What exists | Stars |
|---|---|---|
| Native `.pptx` design linter | leppardwang/pptx-lint, TomiLabo/tmng-pptx-linter | ≤1 |
| Slidev-only linter | Th3Mouk/slidev-linter | ~3 |
| Markdown “presentation checklist” gists | several personal lists | 0–2 |

## What v0.2 adds vs thin skeletons

Most “linters” stop at char-count heuristics. **decklint v0.2** ships:

- WCAG relative-luminance contrast for solid RGB text/fills
- OOXML timing/transition parse + safe strip (`--fix`)
- Layout geometry: occupancy, near-miss alignment, box overlap
- Color / typeface budgets, canvas 16:9 gate
- Chart 3D junk + callout reminder
- a11y preset (alt text + stricter contrast)
- SARIF for GitHub Code Scanning, HTML report, bilingual CLI

## Positioning

**Generators propose. pptx-eslint disposes.**

Demand driver: AI multiplies deck output; quality collapses; teams need CI for slides the same way they needed ESLint when codegen exploded.
