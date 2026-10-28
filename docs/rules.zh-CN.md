# decklint 规则（v0.2）

English → [`rules.md`](rules.md)

分类：`design` · `typography` · `color` · `layout` · `chart` · `animation` · `a11y`

| 规则 id | check 键 | 分类 | 默认级别 | 作用 |
|---|---|---|---|---|
| `max-text` | `max_chars_per_slide` | typography | error | 字符数对照预设上限（反幻灯片文档化） |
| `no-slideument` | `bullet_wall` | typography | error | 子弹过多/过长 |
| `min-font` | `min_font_pt` | typography | error | 显式 run 最小字号 |
| `font-families` | `font_families` | typography | warning | 超过 3 种字体 |
| `accent-colors` | `max_accent_colors` | color | warning | 非近灰强调色数量 |
| `text-contrast` | `text_bg_contrast` | a11y | error | 可解析纯色 RGB 时的 WCAG 对比度 |
| `occupancy` | `occupancy` | layout | warning | 形状总面积 / 幻灯片面积 > 0.72 |
| `alignment-near-miss` | `near_miss_alignment` | layout | warning | 左边距相差 2–8pt 未对齐 |
| `box-overlap` | `box_overlap` | layout | warning | 不透明形状重叠超阈值 |
| `image-bleed` | `image_layout` | layout | info | 单页图片过多 |
| `one-idea` | `max_title_boxes` | design | error | 顶部文本框过多 |
| `title-as-claim` | `title_is_claim` | design | warning | 空泛标题（Overview / 概况 / 目录…） |
| `canvas` | `canvas_ratio` | design | warning/info | 优先约 16:9；4:3 提示 |
| `chart-junk` | `chart_junk` | chart | warning/info | 3D 图表；标注提醒 |
| `animation-policy` | `animation_policy` | animation | warning | 禁用 bounce/spiral 等；限制切换种类 |
| `image-alt` | `image_alt` | a11y | warning（a11y 预设为 error） | 图片缺少 descr/alt |
| `a11y-title` | `a11y_title` | a11y | info/warning | 带标题版式无标题文字 |

## 预设

- **stage** — 现场：最多 80 字符，最小 24pt
- **reading** — 异步：最多 220 字符，最小 14pt
- **keynote** — 继承 stage：最多 40 字符，1 强调色
- **a11y** — 合并 `accessibility.yaml`：更严对比度 + 强制 alt

## 自动修复

仅 OOXML 中可识别的 `animation-policy` 禁用动画/切换可用 `--fix` 剥离。其余仅报告。
