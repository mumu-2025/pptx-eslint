# decklint rules (v0.3)

中文 → [`rules.zh-CN.md`](rules.zh-CN.md)

Categories: `design` · `typography` · `color` · `layout` · `chart` · `animation` · `a11y`

| Rule id | Check key | Category | Severity (default) | What it does |
|---|---|---|---|---|
| `max-text` | `max_chars_per_slide` | typography | error | Char count vs preset max (anti-slideument) |
| `no-slideument` | `bullet_wall` | typography | error | Too many / too long bullets |
| `min-font` | `min_font_pt` | typography | error | Smallest explicit run size vs floor |
| `font-families` | `font_families` | typography | warning | >N distinct typefaces (default 3) |
| `font-embed` | `font_embed` | typography | info (warning in corporate) | OOXML embedded fonts / embed flags |
| `bullet-depth` | `bullet_depth` | typography | warning | Nested paragraph level too deep |
| `accent-colors` | `max_accent_colors` | color | warning | Distinct non-near-gray RGB accents |
| `text-contrast` | `text_bg_contrast` | a11y | error | WCAG ratio when solid RGB resolvable |
| `occupancy` | `occupancy` | layout | warning | Σ shape area / slide area > 0.72 |
| `alignment-near-miss` | `near_miss_alignment` | layout | warning | Left edges 2–8pt apart but not equal |
| `box-overlap` | `box_overlap` | layout | warning | Opaque shape overlap above ratio |
| `image-bleed` | `image_layout` | layout | info | Too many pictures on one slide |
| `safe-margins` | `safe_margins` | layout | warning | Content intrudes ~5% outer margin |
| `max-shapes` | `max_shapes` | layout | warning | Too many shapes (clutter) |
| `one-idea` | `max_title_boxes` | design | error | Many top text frames |
| `title-as-claim` | `title_is_claim` | design | warning | Vague titles (Overview / 概况 / 目录…) |
| `title-length` | `title_length` | design | info | Title too short or too long |
| `empty-slide` | `empty_slide` | design | info | No text / picture / chart |
| `speaker-notes` | `speaker_notes` | design | info (warning in async-doc) | Content slides lack notes |
| `canvas` | `canvas_ratio` | design | warning/info | Prefer ~16:9; info for 4:3 |
| `chart-junk` | `chart_junk` | chart | warning/info | 3D chart types; callout reminder |
| `notes-for-charts` | `notes_for_charts` | chart | info/warning | Chart without explanatory notes |
| `animation-policy` | `animation_policy` | animation | warning | Ban bounce/spiral/…; cap transition variety |
| `image-alt` | `image_alt` | a11y | warning (error in a11y) | Picture missing descr/alt |
| `a11y-title` | `a11y_title` | a11y | info/warning | Titled layout without title text |
| `unique-titles` | `unique_titles` | a11y | warning (error in wcag-strict) | Duplicate or missing titles |
| `vague-links` | `vague_links` | a11y | warning | Vague hyperlink labels |
| `auto-advance` | `auto_advance` | a11y | warning (error in wcag-strict) | Timed `advTm` advance |
| `deck-properties` | `deck_properties` | a11y | info/warning | Empty core Title |

## Presets

- **stage** — live talk: max 80 chars, min 24pt
- **reading** — async: max 220 chars, min 14pt
- **keynote** — extends stage: max 40 chars, 1 accent
- **a11y** — merges `accessibility.yaml`: stricter contrast + alt required
- **corporate** — merges `corporate.yaml`: brand fonts/accents/margins/embed/Title
- **wcag-strict** — merges a11y + `wcag-strict.yaml`: unique titles / alt / auto-advance as errors
- **async-doc** — merges `async-doc.yaml`: speaker notes required on content slides

## Sources (checkable heuristics only)

- Duarte grids / visual system (margins, few fonts/colors)
- Presentation Zen / Reynolds (density, whitespace, one idea)
- Microsoft + university PowerPoint accessibility checklists (unique titles, alt, contrast, on-click advance, descriptive links, notes for charts)
- Corporate brand deck QA (embed fonts, file Title, safe area)

## Auto-fix

Only `animation-policy` offenders that are identifiable in OOXML timing/transition nodes can be stripped with `--fix`. Everything else is report-only.
