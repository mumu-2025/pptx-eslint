# decklint 规则（v0.3）

English → [`rules.md`](rules.md)

分类：`design` · `typography` · `color` · `layout` · `chart` · `animation` · `a11y`

| 规则 id | check 键 | 分类 | 默认级别 | 做什么 |
|---|---|---|---|---|
| `max-text` | `max_chars_per_slide` | typography | error | 每页字符数上限（反幻灯片文档化） |
| `no-slideument` | `bullet_wall` | typography | error | 子弹过多 / 过长 |
| `min-font` | `min_font_pt` | typography | error | 最小显式字号 |
| `font-families` | `font_families` | typography | warning | 字体种类超限（默认 3） |
| `font-embed` | `font_embed` | typography | info（corporate 为 warning） | OOXML 是否嵌入字体 |
| `bullet-depth` | `bullet_depth` | typography | warning | 项目符号嵌套过深 |
| `accent-colors` | `max_accent_colors` | color | warning | 非近灰强调色数量 |
| `text-contrast` | `text_bg_contrast` | a11y | error | 可解析纯色 RGB 的 WCAG 对比度 |
| `occupancy` | `occupancy` | layout | warning | 占版率 > 0.72 |
| `alignment-near-miss` | `near_miss_alignment` | layout | warning | 左边距差 2–8pt 未对齐 |
| `box-overlap` | `box_overlap` | layout | warning | 不透明重叠超阈值 |
| `image-bleed` | `image_layout` | layout | info | 单页图片过多 |
| `safe-margins` | `safe_margins` | layout | warning | 侵入约 5% 外边距 |
| `max-shapes` | `max_shapes` | layout | warning | 形状过多（拥挤） |
| `one-idea` | `max_title_boxes` | design | error | 顶部文本框过多 |
| `title-as-claim` | `title_is_claim` | design | warning | 空泛标题 |
| `title-length` | `title_length` | design | info | 标题过短或过长 |
| `empty-slide` | `empty_slide` | design | info | 空白页 |
| `speaker-notes` | `speaker_notes` | design | info（async-doc 为 warning） | 内容页缺备注 |
| `canvas` | `canvas_ratio` | design | warning/info | 优先约 16:9 |
| `chart-junk` | `chart_junk` | chart | warning/info | 3D 图表；标注提醒 |
| `notes-for-charts` | `notes_for_charts` | chart | info/warning | 图表缺说明备注 |
| `animation-policy` | `animation_policy` | animation | warning | 禁用装饰动画；限制切换种类 |
| `image-alt` | `image_alt` | a11y | warning（a11y 为 error） | 图片缺 alt |
| `a11y-title` | `a11y_title` | a11y | info/warning | 带标题版式无标题 |
| `unique-titles` | `unique_titles` | a11y | warning（wcag-strict 为 error） | 标题重复或缺失 |
| `vague-links` | `vague_links` | a11y | warning | 含糊超链接文案 |
| `auto-advance` | `auto_advance` | a11y | warning（wcag-strict 为 error） | 定时自动进片 |
| `deck-properties` | `deck_properties` | a11y | info/warning | 核心 Title 为空 |

## 预设

- **stage** — 现场：最多 80 字符，最小 24pt
- **reading** — 异步：最多 220 字符，最小 14pt
- **keynote** — 扩展 stage：最多 40 字符，1 个强调色
- **a11y** — 合并 `accessibility.yaml`
- **corporate** — 合并 `corporate.yaml`：品牌字体/强调色/边距/嵌字/Title
- **wcag-strict** — 合并 a11y + `wcag-strict.yaml`
- **async-doc** — 合并 `async-doc.yaml`：内容页强制备注

## 自动修复

仅可从 OOXML 识别的 `animation-policy` 禁用动画/切换可用 `--fix` 剥离。其余均为报告项。
