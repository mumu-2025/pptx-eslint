# decklint rules (v0.2)

中文 → [`rules.zh-CN.md`](rules.zh-CN.md)

Categories: `design` · `typography` · `color` · `layout` · `chart` · `animation` · `a11y`

| Rule id | Check key | Category | Severity (default) | What it does |
|---|---|---|---|---|
| `max-text` | `max_chars_per_slide` | typography | error | Char count vs preset max (anti-slideument) |
| `no-slideument` | `bullet_wall` | typography | error | Too many / too long bullets |
| `min-font` | `min_font_pt` | typography | error | Smallest explicit run size vs floor |
| `font-families` | `font_families` | typography | warning | >3 distinct typefaces |
| `accent-colors` | `max_accent_colors` | color | warning | Distinct non-near-gray RGB accents |
| `text-contrast` | `text_bg_contrast` | a11y | error | WCAG ratio when solid RGB resolvable; 4.5 body / 3.0 large |
| `occupancy` | `occupancy` | layout | warning | Σ shape area / slide area > 0.72 |
| `alignment-near-miss` | `near_miss_alignment` | layout | warning | Left edges 2–8pt apart but not equal |
| `box-overlap` | `box_overlap` | layout | warning | Opaque shape overlap above ratio |
| `image-bleed` | `image_layout` | layout | info | Too many pictures on one slide |
| `one-idea` | `max_title_boxes` | design | error | Many top text frames |
| `title-as-claim` | `title_is_claim` | design | warning | Vague titles (Overview / 概况 / 目录…) |
| `canvas` | `canvas_ratio` | design | warning/info | Prefer ~16:9; info for 4:3 |
| `chart-junk` | `chart_junk` | chart | warning/info | 3D chart types; callout reminder |
| `animation-policy` | `animation_policy` | animation | warning | Ban bounce/spiral/…; cap transition variety |
| `image-alt` | `image_alt` | a11y | warning (error in a11y) | Picture missing descr/alt |
| `a11y-title` | `a11y_title` | a11y | info/warning | Titled layout without title text |

## Presets

- **stage** — live talk: max 80 chars, min 24pt
- **reading** — async: max 220 chars, min 14pt
- **keynote** — extends stage: max 40 chars, 1 accent
- **a11y** — merges `accessibility.yaml`: stricter contrast + alt required

## Auto-fix

Only `animation-policy` offenders that are identifiable in OOXML timing/transition nodes can be stripped with `--fix`. Everything else is report-only.
